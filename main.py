import sqlite3
from SQLITE_Queries import *
from SQLITE_Queries import dict_comp
import func_sent
import Preset_script

# you can download the full database here as long as you sign in with a tue account I think:
# https://tuenl-my.sharepoint.com/:f:/g/personal/f_w_overbeeke_student_tue_nl/EpB5TC5jDjpImyD3pco6UeoBbUvfWgpszLe2qjdO7_bwrA?e=XE6cQC
# link to folder containing the database in several ways

# initializing variables
comparison = []


def full_program():
    while 1:
        choice = input("\nChoose one of the following actions:\n"
                       " - Type 'a' to add company table\n"
                       " - Type 'd' to delete\n"
                       " - Type 'e' to run sentiment analysis on a table\n"
                       " - Type 'q' to quit \n")
        if choice == 'a':
            company = input("Type the screenname of the company:\n")
            if company in [i[0] for i in dict_comp]:
                add_company(company, conn, cursor)
            if company not in [i[0] for i in dict_comp]:
                print('NOT FOUND, TRY AGAIN')
        elif choice == 'd':
            table = input("Name of table you want to delete:\n")
            if table == 'main' or table == 'replies' or table == 'user':
                print("Don't delete those you fool!")
            else:
                cursor.execute("DROP TABLE " + table + ";")
        elif choice == 'e':
            table = input("Name of the company you want to evaluate:\n")
            func_sent.add_sentiment(table, conn, cursor)
        elif choice == 'q':
            print("✌(◕‿-)✌")
            return
        else:
            print('You probably mistyped, try again')


while 1:
    toggle = input('Do you want to: \n'
                   ' - Create a new database? (n) \n'
                   ' - Work with the full database? (f) \n'
                   ' - Work with the September database? (s)\n'
                   ' - Specify month and run a preset? (p)\n')
    if toggle == 'n':
        conn = sqlite3.connect('DataChallenge.sqlite')
        cursor = conn.cursor()
        exec(open('EFFICIENT_LOADING.py').read())
        cursor.execute(QUERY_DUPLICATES)
        cursor.execute(QUERY_DUP_USER)
        cursor.executescript(QUERY_REPLY_TABLES)
        conn.commit()
        full_program()
        break
    elif toggle == 'f':
        # specificeer hieronde waar ALL_DATA.sqlite staat
        conn = sqlite3.connect("D:\\EXPORT\\ALL_DATA.sqlite")
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        full_program()
        break
    elif toggle == 's':
        # specificeer hieronde waar SeptData.sqlite staat
        conn = sqlite3.connect("D:\\EXPORT\\SeptData.sqlite")
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        full_program()
        break
    elif toggle == 'p':
        Preset_script.preset_script_full()
        print("✌(◕‿-)✌")
        break
    else:
        print("Try typing 'n', 'f' or 's' \n")

