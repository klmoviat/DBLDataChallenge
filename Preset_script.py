import sqlite3

import def_plots
from SQLITE_Queries import *
from func_sent import *
import numpy as np
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt


def preset_script_full():
    filepath = "D:\\EXPORT\\PRESET.sqlite"
    if os.path.exists(filepath):
        os.remove(filepath)
    old_db = "D:\\EXPORT\\ALL_DATA.sqlite"
    shutil.copy(old_db, filepath)
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.executescript(QUERY_DROP)
    month = input("Which month would you like to run ? (Jan, Feb, etc.)\n")
    cursor.execute("create table 'preset_main' as select * from main where strftime('%m', created_at) = ?",
                   (eval(month), ))
    # cursor.execute("create table 'preset_replies' as select * from main.replies"
    #                " inner join main on KLM.head = id_str where strftime('%m', created_at) = ?",
    #                (eval(month),))
    cursor.execute("create table 'preset_KLM' as select * from KLM"
                   " inner join main on KLM.head = id_str where strftime('%m', created_at) = ?",
                   (eval(month),))
    cursor.execute("create table 'preset_British_Airways' as select * from British_Airways"
                   " inner join main on head = id_str where strftime('%m', created_at) = ?",
                   (eval(month),))
    cursor.execute("create table 'preset_Lufthansa' as select * from Lufthansa"
                   " inner join main on head = id_str where strftime('%m', created_at) = ?",
                   (eval(month),))
    cursor.execute("create table 'preset_RyanAir' as select * from Ryanair"
                   " inner join main on head = id_str where strftime('%m', created_at) = ?",
                   (eval(month),))
    cursor.execute("drop table main")
    cursor.execute("drop table Lufthansa")
    cursor.execute("drop table RyanAir")
    cursor.execute("drop table KLM")
    cursor.execute("drop table British_Airways")

    # cursor.execute("alter table preset_replies rename to replies")
    cursor.execute("alter table preset_main rename to main")
    cursor.execute("alter table preset_KLM rename to KLM")
    cursor.execute("alter table preset_British_Airways rename to British_Airways")
    cursor.execute("alter table preset_Lufthansa rename to Lufthansa")
    cursor.execute("alter table preset_RyanAir rename to RyanAir")

    def_plots.avg_bar_plot(conn, cursor, month)
    def_plots.bar_box_count(conn, cursor)
    def_plots.violin_sentiment(conn, cursor)
