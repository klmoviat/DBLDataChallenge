klm='56377143'
brittish='18332190'


QUERY_REPLY= "CREATE TABLE 'replies' AS SELECT id_str, in_reply_to_status_id_str " \
            "FROM main where in_reply_to_status_id_str is not NULL and id_str is not NULL;"

QUERY_DUPLICATES="delete from main where rowid not in ( select min(rowid)from main group by id_str)"

QUERY_DUP_USER="DELETE FROM user where rowid not in (select  min(rowid) from user group by id)"

QUERY_CREATION_TWEET="SELECT main.created_at FROM main, replies where main.id_str is replies.id_str;"

QUERY_CREATION_REPLY="SELECT main.created_at FROM main, replies where main.id_str is replies.id_str;"
