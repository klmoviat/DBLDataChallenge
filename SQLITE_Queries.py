klm='56377143'
brittish='18332190'


#QUERY_REPLY= "CREATE TABLE 'replies' AS SELECT id_str, in_reply_to_status_id_str " \
            #"FROM main where in_reply_to_status_id_str is not NULL and id_str is not NULL;"

QUERY_DUPLICATES="delete from main where rowid not in ( select min(rowid)from main group by id_str)"

QUERY_DUP_USER="DELETE FROM user where rowid not in (select  min(rowid) from user group by id)"

#QUERY_CREATION_TWEET="SELECT main.created_at FROM main, replies where main.id_str is replies.id_str;"

#QUERY_CREATION_REPLY="SELECT main.created_at FROM main, replies where main.id_str is replies.id_str;"

QUERY_REPLY_TABLES= """
DROP TABLE IF EXISTS `temp_replies`;
DROP TABLE IF EXISTS `temp`;
DROP TABLE IF EXISTS `replies`;
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