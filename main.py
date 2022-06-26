import sqlite3

import sentiment_on_main
from SQLITE_Queries import *
from SQLITE_Queries import dict_comp
import func_sent
from func_sent import tokenizer, tokenizer_nl, model, model_nl
import Preset_script
from def_plots import *
from tkinter import *
from tkinter import Tk
from tkinter import filedialog as fd
from tkinter import ttk
# you can download the full database here as long as you sign in with a tue account I think:
# https://tuenl-my.sharepoint.com/:f:/g/personal/f_w_overbeeke_student_tue_nl/EpB5TC5jDjpImyD3pco6UeoBbUvfWgpszLe2qjdO7_bwrA?e=XE6cQC
# link to folder containing the database in sever   al ways

# initializing variables
comparison = []
filename = ''


# Create UI for selecting database location
def database_location(prompt):
    def browse_files():
        global filename
        filename = fd.askopenfilename()
        # Change label contents
        label_file_explorer.configure(text="File Opened: " + filename)

    def close_win():
        root.destroy()
    # Create the root window
    root = Tk()
    # Set window title
    root.title(prompt)

    # Set window size
    root.geometry("700x300")

    # Create a File Explorer label
    label_file_explorer = Label(root,
                                text="Select the database",
                                width=100, height=4,
                                fg="blue")

    button_explore = Button(root,
                            text="Browse Files",
                            command=browse_files)

    button_exit = Button(root,
                         text="Confirm",
                         command=close_win)

    label_file_explorer.grid(column=1, row=1)
    button_explore.grid(column=1, row=2)
    button_exit.grid(column=1, row=3)
    root.attributes('-topmost', 1)
    root.mainloop()


# The full program that interacts with the databases
def full_program():
    while 1:
        choice = input("\nChoose one of the following actions:\n"
                       " - Type 'a' to add company table\n"
                       " - Type 'd' to delete a table\n"
                       " - Type 'e' to run sentiment analysis on a table\n"
                       " - Type 'm' to run sentiment analysis on main\n"
                       " - Type 'p' to make the plots\n"
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
        elif choice == 'm':
            print('This will take up to 10 hours for the full database!')
            sentiment_on_main.sentiment_on_main(conn, cursor, tokenizer, model, tokenizer_nl, model_nl)
        elif choice == 'p':
            avg_bar_plot(conn, cursor)
            violin_sentiment(conn, cursor)
            bar_box_count(conn, cursor)
            sentiment_year(conn, cursor)
            med_response(cursor, conn)
        elif choice == 'q':
            print("✌(◕‿-)✌")
            return
        else:
            print('You probably mistyped, try again')


# The start of the program that asks for the database
while 1:
    toggle = input('Do you want to: \n'
                   ' - Create a new database? (n) \n'
                   ' - Work with a specific database? (s) \n'
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
    elif toggle == 's':
        # specificeer hieronde waar ALL_DATA.sqlite staat
        database_location('Select the database you want to work on')
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        print('DO NOT FORGET TO FIRST DROP COMPANY TABLES!')
        print('List of available tables:')
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        full_program()
        break
    elif toggle == 'p':
        database_location('Select the full database')
        Preset_script.preset_script_full(filename)
        print("✌(◕‿-)✌")
        break
    else:
        print("Try typing 'n', 'f' or 's' \n")

