dict_comp = [('KLM', '56377143'),
('AirFrance', '106062176'),
('British_Airways', '18332190'),
('AmericanAir', '22536055'),
('Lufthansa', '124476322'),
('AirBerlin', '26223583'),
('AirBerlin_assist', '2182373406'),
('easyJet', '38676903'),
('RyanAir', '1542862735'),
('SingaporeAir', '253340062'),
('Qantas', '218730857'),
('EtihadAirways', '45621423'),
('VirginAtlantic', '20626359')]

Jan = '01'
Feb = '02'
Mar = '03'
Apr = '04'
May = '05'
Jun = '06'
Jul = '07'
aug = '08'
Sep = '09'
Oct = '10'
Nov = '11'
Dec = '12'
comp = ''


def add_company(company, conn, cursor):
    comp_id = [i[1] for i in dict_comp if i[0] == company][0]
    cursor.executescript(QUERY_part_1)
    cursor.execute(QUERY_part_2, (comp_id,))
    cursor.execute(QUERY_part_3)
    cursor.execute(QUERY_part_4, (comp_id,))
    cursor.executescript(QUERY_part_5)
    cursor.execute(QUERY_part_7, (comp_id,))
    cursor.executescript(QUERY_part_8)
    cursor.executescript(QUERY_HEAD_TAIL_TEXT)
    cursor.execute("ALTER TABLE head_tail RENAME TO " + company + ";")
    conn.commit()

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
DROP TABLE IF EXISTS `temp1`;
DROP TABLE IF EXISTS `replies`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_head_tail`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_text`;
DROP TABLE IF EXISTS `A`;
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
#combine with head_tail_text to get the text as well
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

#QUERY WAARBIJ DE TAIL NOOIT COMPANY IS
QUERY_part_1 = """
DROP TABLE IF EXISTS `temp_replies`; /*drop old tables*/
DROP TABLE IF EXISTS `temp`;
DROP TABLE IF EXISTS `temp1`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_head_tail`;
DROP TABLE IF EXISTS `head_tail`;
DROP TABLE IF EXISTS `temp_text`;
DROP TABLE IF EXISTS `A`;
    create table temp_head_tail as /*create temp tabel met de staart van convo*/
        select
            id_str as tail_id
        from replies
        where id_str NOT IN  (select in_reply_to_status_id_str from replies);
    
    create table 'A' as select temp_head_tail.tail_id, replies.in_reply_to_status_id_str, user_id /*CREATE TABLE*/
        from temp_head_tail             /*HIERIN STAAN DE CURRENT TAIL, HETGEEN WAAR HET OP REPLIED EN USERID VAN TAIL*/
        inner join replies on replies.id_str=temp_head_tail.tail_id
        inner join main on main.id_str = replies.id_str;
"""
    
QUERY_part_2 = "UPDATE A set tail_id = A.in_reply_to_status_id_str where user_id = ?;"

QUERY_part_3 = "drop table 'temp_head_tail';    /*MAAK TEMP_HEAD_TAIL OPNIEUW*/"

QUERY_part_4 = "create table 'temp_head_tail' as select tail_id as tail_id from A inner join main on A.tail_id = main.id_str where main.in_reply_to_user_id_str = ?;"

#Volledige conversations inladen met alle stappen
QUERY_part_5 = """
    drop table A;
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
    ;
    

"""

# Delete all heads that are the company itself, so the heads start with 1st user tweet
QUERY_part_7 = """delete from head_tail where head_tail.temp_head in
    (
        select q.temp_head
            from (
            select h.temp_head, max(h.depth), h.tail_id
            from head_tail h
            group by h.tail_id
            INTERSECT SELECT
            h.temp_head, depth, h.tail_id
            from head_tail h
            inner join main on main.id_str = h.temp_head
            where main.user_id = ?
            ) q
        );"""

# creating a table head_tail with the end head and tail from convo, with both same user and must be conversation
QUERY_part_8 = """
    CREATE TABLE 'temp1' as 
    SELECT head_tail.temp_head as head, head_tail.tail_id, max(head_tail.depth) as depth
    FROM head_tail
    GROUP BY head_tail.tail_id;
    
    CREATE TABLE 'temp' as 
    SELECT temp1.head, temp1.tail_id, max(temp1.depth) as depth
    FROM temp1
    GROUP BY temp1.head;
    DROP TABLE IF EXISTS `temp1`;
    DELETE FROM temp where depth < 2;
    
    DROP TABLE head_tail;
    
    CREATE TABLE 'head_tail' as
        select * from temp A where (
            select main.user_id
            from temp A2
            inner join main on main.id_str = a.head
                                              ) = (
                                                  select main.user_id
                                                    from temp A2
                                                    inner join main on main.id_str = a.tail_id
    );          
    DROP TABLE temp;
    
"""

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
        inner join head_tail on head_tail.head=main.id_str
        ) head on head.row_num=tail.row_num
    order by head.row_num;

    create table 'temp_head_tail' as /*maak een tijdelijke tabel aan waarin head_tailen*/
    select                           /*de tabel hierboven gecombineerd worden*/
        head_tail.head,
        temp_text.head_text,
        head_tail.tail_id,
        temp_text.tail_text,
        head_tail.depth,
        row_number() over (order by(select NULL)) as CONV_ID
    from (  
        select head_tail.head, head_tail.tail_id, head_tail.depth, row_number() over (order by tail_id, head)
         as row_num from head_tail)head_tail
        inner join (
            select head_text, tail_text, row_number() over (order by (select null)) as row_num from temp_text)temp_text
        on head_tail.row_num=temp_text.row_num;
    
    drop table head_tail; /*verwijder oude tabellen*/
    drop table temp_text;
    ALTER TABLE temp_head_tail RENAME TO head_tail /*rename temp tabel naar de hoofd tabel*/
    ;"""


#drop tables queries
QUERY_DROP = """
    drop table if exists KLM;
    drop table if exists British_Airways;
    drop table if exists Lufthansa;
    drop table if exists RyanAir;
    drop table if exists head_tail;
    drop table if exists temp_head_tail;
"""

QUERY_KLM_TWEETS = """
    DROP TABLE IF EXISTS new_table;
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS new_table( 
       KLM, 
       BA, 
       LH, 
       RA
    );
    INSERT INTO new_table(KLM)
        SELECT id_str 
        FROM main
        WHERE user_id = 56377143;
    INSERT INTO new_table(BA)
        SELECT id_str
        FROM main
        WHERE user_id = 18332190;
    INSERT INTO new_table(LH)
        SELECT id_str 
        FROM main
        WHERE user_id = 124476322;
    INSERT INTO new_table(RA)
        SELECT id_str 
        FROM main
        WHERE user_id = 1542862735;
    COMMIT;
    PRAGMA foreign_keys=on;
"""

QUERY_RESPONSE_TIME = """
    DROP TABLE IF EXISTS response_times;
    
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS response_times( 
       KLM, 
       BA, 
       LH, 
       RA
    );
    INSERT INTO response_times(KLM)
        SELECT replies.response_time
        FROM replies, new_table
        WHERE new_table.KLM = replies.id_str;
    INSERT INTO response_times(BA)
        SELECT replies.response_time
        FROM replies, new_table
        WHERE new_table.BA = replies.id_str;
    INSERT INTO response_times(LH)
        SELECT replies.response_time
        FROM replies, new_table
        WHERE new_table.LH = replies.id_str;
    INSERT INTO response_times(RA)
        SELECT replies.response_time
        FROM replies, new_table
        WHERE new_table.RA = replies.id_str;
    COMMIT;
    PRAGMA foreign_keys=on;
    DROP TABLE IF EXISTS new_table;
"""