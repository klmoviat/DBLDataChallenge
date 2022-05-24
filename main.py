# This is a sample Python script
# Press the green button in the gutter to run the script.
from typing import Any

import pandas as pd
import sqlite3
from SQLITE_Queries import *
from datetime import datetime
# you can download the full database here as long as you sign in with a tue account i think:
# https://tuenl-my.sharepoint.com/:u:/g/personal/f_w_overbeeke_student_tue_nl/Eb1QH0eCbehHvQQFp8FEzqgBHo8UsNsZEY9LdlTNVXTtXw?e=mebZzs
# this is the 2.78 gb file containing the main table, user table and replies table
# import it in pycharm using the '+' button at the database tab right from here
while 1:
    ask = input('Create new database or run over existing? (n/e) ')
    if ask == 'n':

        conn = sqlite3.connect('DataChallenge.sqlite')
        cursor = conn.cursor()
        exec(open('EFFICIENT_LOADING.py').read())
        cursor.execute(QUERY_DUPLICATES)
        cursor.execute(QUERY_DUP_USER)
        cursor.executescript(QUERY_REPLY_TABLES)
        break
    if ask == 'e':
        conn = sqlite3.connect('ALL_DATA.sqlite')
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        break
    else:
        print("Try typing 'n' or 'e' \n")

while 1:
    toggle = input("Type a to add company table OR d to delete OR q to quit: ")
    if toggle == 'a':
        comp = input("Type the screenname of the company: ")
        if comp in dir():
            comp_id = eval(comp)
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
    if toggle == 'd':
        table = input("Name of table you want to delete: ")
        cursor.execute("DROP TABLE " + table + ";")
    if toggle == 'q':
        break
