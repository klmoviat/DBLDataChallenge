# This is a sample Python script
# Press the green button in the gutter to run the script.
from typing import Any

import pandas as pd
import sqlite3
from SQLITE_Queries import *
import numpy as np

from datetime import datetime
# you can download the full database here as long as you sign in with a tue account I think:
# https://tuenl-my.sharepoint.com/:u:/g/personal/f_w_overbeeke_student_tue_nl/Eb1QH0eCbehHvQQFp8FEzqgBHo8UsNsZEY9LdlTNVXTtXw?e=mebZzs
# this is the 2.78 gb file containing the main table, user table and replies table
# import it in pycharm using the '+' button at the database tab right from here
while 1:
    ask = input('Create new database or work with the full database? (n/f)\n')
    if ask == 'n':
        conn = sqlite3.connect('DataChallenge.sqlite')
        cursor = conn.cursor()
        exec(open('EFFICIENT_LOADING.py').read())
        cursor.execute(QUERY_DUPLICATES)
        cursor.execute(QUERY_DUP_USER)
        cursor.executescript(QUERY_REPLY_TABLES)
        break
    if ask == 'f':
        # specificeer hieronde waar ALL_DATA.sqlite staat
        conn = sqlite3.connect("D:\\EXPORT\\ALL_DATA.sqlite")
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        break
    else:
        print("Try typing 'n' or 'f' \n")

while 1:
    toggle = input("Choose one of the following actions:\n"
                   " - Type 'a' to add company table\n"
                   " - Type 'd' to delete\n"
                   " - Type 'e' to evaluate a table\n"
                   " - Type 'q' to quit: \n")
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
            # cursor.execute("CREATE TABLE " + conv_name + " as SELECT * FROM head_tail;")
            cursor.execute(QUERY_part_7, (comp_id,))
            cursor.executescript(QUERY_part_8)
            cursor.executescript(QUERY_HEAD_TAIL_TEXT)
            cursor.execute("ALTER TABLE head_tail RENAME TO " + comp + ";")
            conn.commit()
        if comp not in dir():
            print('NOT FOUND, TRY AGAIN')
    if toggle == 'd':
        table = input("Name of table you want to delete:\n")
        if table == 'main' or table == 'replies' or table == 'user':
            print("Don't delete those you fool!")
        else:
            cursor.execute("DROP TABLE " + table + ";")
    if toggle == 'e':
        table = input("Name of the company you want to evaluate:\n")
        HEAD = cursor.execute("SELECT head_text from " + table).fetchall()
        head = [i[0] for i in HEAD]
        TAIL = cursor.execute("SELECT tail_text from " + table).fetchall()
        tail = [i[0] for i in TAIL]
        all_scores = []
        for x in head:
            score = function(head[x], tail[x])   #pass iedere head en tail aan eval functie?
            all_scores = all_scores.append(score)   #maak een lijst met alle scores?
        print(np.average(all_scores))       #print average?
    if toggle == 'q':
        print("(° ͜ʖ͡°)╭∩╮")
        break
