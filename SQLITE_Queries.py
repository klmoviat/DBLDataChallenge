# place to store known id's of users
KLM = '56377143'
AirFrance = '106062176'
British_Airways = '18332190'
AmericanAir = '22536055'
Lufthansa = '124476322'
AirBerlin = '26223583'
AirBerlin_assist = '2182373406'
easyJet = '38676903'
RyanAir = '1542862735'
SingaporeAir = '253340062'
Qantas = '218730857'
EtihadAirways = '45621423'
VirginAtlantic = '20626359'


# delete duplicates in main table. NOTE: these duplicates are due to
# the last x entries in a file also being the first x in the next file
# i don't think filtering this at creation stage is faster?
QUERY_DUPLICATES = "delete from main where rowid not in ( select min(rowid)from main group by id_str)"

# delete duplicate entries in user table
QUERY_DUP_USER = "DELETE FROM user where rowid not in (select  min(rowid) from user group by id)"

# add table with id's of each tweet that is a response, the response id and the response time
QUERY_REPLY_TABLES = """
DROP TABLE IF EXISTS `temp_replies`; /*drop old tables*/
DROP TABLE IF EXISTS `temp`;
DROP TABLE IF EXISTS `replies`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_head_tail`;
CREATE TABLE 'temp_replies' AS/*create temp table with tweets, in reply to en timestamp van tweet*/
    SELECT
        id_str,
        in_reply_to_status_id_str,
        created_at
FROM main
    where in_reply_to_status_id_str is not NULL AND in_reply_to_status_id_str in (select id_str FROM main);

create table 'temp' as /*extract de timestamp van de reply uit main, en bereken response time*/
    select main.created_at as created_tweet,
    main.id_str,
    (select round((julianday(temp_replies.created_at)-julianday(main.created_at))*1440))as response_time,
    temp_replies.created_at
    FROM main
        INNER JOIN temp_replies ON temp_replies.in_reply_to_status_id_str = main.id_str
    order by main.id_str;

create table 'replies' as   /*combineer de twee tabellen hierboven*/
select replies.id_str,
       replies.in_reply_to_status_id_str,
       replies.created_at,
       temp.created_tweet as created_original,
       temp.response_time
from(
    SELECT id_str, created_tweet,response_time,row_number() over (order by id_str) as row_num
    FROM temp)temp
join
    (SELECT in_reply_to_status_id_str, id_str,created_at,row_number() over (order by in_reply_to_status_id_str)
     as row_num
    FROM temp_replies)replies
on  temp.row_num=replies.row_num;

DROP TABLE temp_replies; /*verwijder de temp tabellen*/
DROP TABLE temp;

"""

# add table with the id's of the tails of the conversations and each level above it untill the head
# and the depth of the conversations
QUERY_HEAD_TAIL = """
    create table temp_head_tail as /*create temp tabel met de staart van convo*/
        select
            id_str as tail_id
        from replies
        where id_str NOT IN  (select in_reply_to_status_id_str from replies);
                    
    CREATE TABLE head_tail AS               /*veel te kutte code om de tails van convos te laden*/
        WITH RECURSIVE cte_head AS (        /*, iedere laag boven de tail en de depth. kan uitleggen als je wilt*/
            select replies.in_reply_to_status_id_str as temp_head,
                   temp_head_tail.tail_id, 1 as depth
            from replies
            inner join temp_head_tail on temp_head_tail.tail_id = replies.id_str
    
            UNION ALL
    
            select replies.in_reply_to_status_id_str as temp_head,
                   cte_head.tail_id, depth+1
            FROM replies
            JOIN cte_head ON cte_head.temp_head = replies.id_str
        )
        SELECT * FROM cte_head  /*selecteer de zojuist gemaakte query voor de table*/
    order by tail_id;           /*order hem bij tail_id voor consistency die later nodig is*/
    DROP TABLE temp_head_tail   /*drop de temp tables weer*/
    ;"""

# add the text to the table with heads and tails of conversations
QUERY_HEAD_TAIL_TEXT = """
    create table 'temp_text' as /*kutcode om de text van de heads en tails van head_tail te laden*/
    select tail.tail_text,
           head.head_text
    from(
        select
        main.text as tail_text,
        row_number() over (order by head_tail.tail_id) as row_num
        from main
        inner join head_tail on head_tail.tail_id=main.id_str
        ) tail
    inner join(
        select
        main.text as head_text,
        row_number() over (order by head_tail.tail_id) as row_num
        from main
        inner join head_tail on head_tail.temp_head=main.id_str
        ) head on head.row_num=tail.row_num
    order by head.row_num;
    
    create table 'temp_head_tail' as /*maak een tijdelijke tabel aan waarin head_tailen*/
    select                           /*de tabel hierboven gecombineerd worden*/
        head_tail.temp_head,
        temp_text.head_text,
        head_tail.tail_id,
        temp_text.tail_text,
        head_tail.depth
    from (  
        select head_tail.temp_head, head_tail.tail_id, head_tail.depth, row_number() over (order by (select null))
         as row_num from head_tail)head_tail
        inner join (
            select head_text, tail_text, row_number() over (order by (select null)) as row_num from temp_text)temp_text
        on head_tail.row_num=temp_text.row_num;
    
    drop table head_tail; /*verwijder oude tabellen*/
    drop table temp_text;
    ALTER TABLE temp_head_tail RENAME TO head_tail /*rename temp tabel naar de hoofd tabel*/
    ;"""