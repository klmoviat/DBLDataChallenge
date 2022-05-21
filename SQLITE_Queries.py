#place to store known id's of users
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


#delete duplicates in main table. NOTE: these duplicates are due to
#the last x entries in a file also being the first x in the next file
#i don't think filtering this at creation stage is faster?
QUERY_DUPLICATES="delete from main where rowid not in ( select min(rowid)from main group by id_str)"

#delete duplicate entries in user table
QUERY_DUP_USER="DELETE FROM user where rowid not in (select  min(rowid) from user group by id)"

#add table with id's of each tweet that is a response, the response id and the response time
QUERY_REPLY_TABLES = """
DROP TABLE IF EXISTS `temp_replies`;
DROP TABLE IF EXISTS `temp`;
DROP TABLE IF EXISTS `replies`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_head_tail`;
CREATE TABLE 'temp_replies' AS
    SELECT
        id_str,
        in_reply_to_status_id_str,
        created_at
FROM main
    where in_reply_to_status_id_str is not NULL AND in_reply_to_status_id_str in (select id_str FROM main);

create table 'temp' as
    select main.created_at as created_tweet,
    main.id_str,
    (select round((julianday(temp_replies.created_at)-julianday(main.created_at))*1440))as response_time,
    temp_replies.created_at
    FROM main
        INNER JOIN temp_replies ON temp_replies.in_reply_to_status_id_str = main.id_str
    order by main.id_str;

create table 'replies' as
select replies.id_str,
       replies.in_reply_to_status_id_str,
       replies.created_at,
       temp.created_tweet as created_original,
       temp.response_time
from(
    SELECT id_str, created_tweet,response_time,row_number() over (order by id_str) as row_num
    FROM temp)temp
join
    (SELECT in_reply_to_status_id_str, id_str,created_at,row_number() over (order by in_reply_to_status_id_str) as row_num
    FROM temp_replies)replies
on  temp.row_num=replies.row_num;

DROP TABLE temp_replies;
DROP TABLE temp;

"""

#add table with the id's of the tails of the conversations and each level above it untill the head
#and the depth of the conversations
QUERY_HEAD_TAIL = """create table temp_head_tail as
                        select
                            id_str as tail_id
                    from replies
                    where id_str NOT IN  (select in_reply_to_status_id_str from replies);
                    
                    CREATE TABLE head_tail AS
    WITH RECURSIVE cte_head AS (
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
    SELECT * FROM cte_head
    order by tail_id;
    DROP TABLE temp_head_tail;"""

#add the text to the table with heads and tails of conversations
QUERY_HEAD_TAIL_TEXT = """
    create table 'temp_head_tail' as
    select
        head_tail.temp_head,
        temp_text.head_text,
        head_tail.tail_id,
        temp_text.tail_text,
        head_tail.depth
    from (
        select temp_head, tail_id, depth, row_number() over (order by (select null)) as row_num from head_tail)head_tail
    inner join (
        select head_text, tail_text, row_number() over (order by (select null)) as row_num from temp_text)temp_text
    on head_tail.row_num=temp_text.row_num;
    
    drop table head_tail;
    drop table temp_text;
    ALTER TABLE temp_head_tail RENAME TO head_tail;
"""