import sqlite3
from SQLITE_Queries import *
from func_sent import *

# you can download the full database here as long as you sign in with a tue account I think:
# https://tuenl-my.sharepoint.com/:f:/g/personal/f_w_overbeeke_student_tue_nl/EpB5TC5jDjpImyD3pco6UeoBbUvfWgpszLe2qjdO7_bwrA?e=XE6cQC
# link to folder containing the database in several ways

# initializing variables
comparison = []
while 1:
    toggle = input('Do you want to: \n'
                   'Create a new database? (n) \n'
                   'Work with the full database? (f) \n'
                   'Work with the September database? (s)\n')
    if toggle == 'n':
        conn = sqlite3.connect('DataChallenge.sqlite')
        cursor = conn.cursor()
        exec(open('EFFICIENT_LOADING.py').read())
        cursor.execute(QUERY_DUPLICATES)
        cursor.execute(QUERY_DUP_USER)
        cursor.executescript(QUERY_REPLY_TABLES)
        conn.commit()
        break
    if toggle == 'f':
        # specificeer hieronde waar ALL_DATA.sqlite staat
        conn = sqlite3.connect("D:\\EXPORT\\ALL_DATA_lang.sqlite")
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        break
    if toggle == 's':
        # specificeer hieronde waar SeptData.sqlite staat
        conn = sqlite3.connect("D:\\EXPORT\\SeptData_lang.sqlite")
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        break
    else:
        print("Try typing 'n', 'f' or 's' \n")

while 1:
    toggle = input("\nChoose one of the following actions:\n"
                   " - Type 'a' to add company table\n"
                   " - Type 'd' to delete\n"
                   " - Type 'e' to run sentiment analysis on a table\n"
                   " - Type 'q' to quit \n")
    if toggle == 'a':
        comp = input("Type the screenname of the company:\n")
        if comp in dir():
            comp_id = eval(comp)
            conv_name = comp + '_full_conv'
            cursor.executescript(QUERY_part_1)
            cursor.execute(QUERY_part_2, (comp_id,))
            cursor.execute(QUERY_part_3)
            cursor.execute(QUERY_part_4, (comp_id,))
            cursor.executescript(QUERY_part_5)
            cursor.execute(QUERY_part_7, (comp_id,))
            cursor.executescript(QUERY_part_8)
            cursor.executescript(QUERY_HEAD_TAIL_TEXT)
            cursor.execute("ALTER TABLE head_tail RENAME TO " + comp + ";")
            conn.commit()
        if comp not in dir():
            print('NOT FOUND, TRY AGAIN')
    elif toggle == 'd':
        table = input("Name of table you want to delete:\n")
        if table == 'main' or table == 'replies' or table == 'user':
            print("Don't delete those you fool!")
        else:
            cursor.execute("DROP TABLE " + table + ";")
    elif toggle == 'e':
        table = input("Name of the company you want to evaluate:\n")
        HEAD = cursor.execute("SELECT head_text, CONV_ID from " + table +
                              " inner join main on head = id_str where lang = 'en'").fetchall()
        head = [i[0] for i in HEAD]
        conv_id = [i[1] for i in HEAD]
        TAIL = cursor.execute("SELECT tail_text from " + table +
                              " inner join main on head = id_str where lang = 'en'").fetchall()
        tail = [i[0] for i in TAIL]
        HEAD_NL = cursor.execute("SELECT head_text, CONV_ID from " + table +
                                 " inner join main on head = id_str where lang = 'nl'").fetchall()
        head_nl = [i[0] for i in HEAD_NL]
        conv_id_nl = [i[1] for i in HEAD_NL]
        TAIL_NL = cursor.execute("SELECT tail_text from " + table +
                                 " inner join main on head = id_str where lang = 'nl'").fetchall()
        tail_nl = [i[0] for i in TAIL_NL]
        result = sentiment_compare(head, tail, conv_id) + sentiment_compare_nl(head_nl, tail_nl, conv_id_nl)
        # comparison = np.asarray(result)
        # mean_change = np.mean(comparison[:, 2]) #mean verandering, maar met absolute termen (1=neg,2=neu,3=pos)
        # mean_first = np.mean(comparison[:, 0])
        # mean_last = np.mean(comparison[:, 1])
        # print("Average first tweet: {} \n".format(mean_first))
        # print("Average last tweet: {} \n".format(mean_last))
        # print("Average change: {}".format(mean_change))
        cursor.execute("ALTER TABLE " + table + " add head_sentiment")
        cursor.execute("ALTER TABLE  " + table + "  add tail_sentiment")
        cursor.execute("ALTER TABLE  " + table + "  add delta_sentiment")
        cursor.executemany("UPDATE  " + table + "  SET head_sentiment = (?), tail_sentiment = (?),"
                                                " delta_sentiment = (?) where CONV_ID = (?)", result)
        conn.commit()
    elif toggle == 'q':
        print("✌(◕‿-)✌")
        break
    else:
        print('You probably mistyped, try again')
