from SQLITE_Queries import *
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def response_times(conn, cursor):
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(17,8))
    KLM_AVG = pd.read_sql(
        'SELECT AVG(KLM) FROM response_times',
        conn)
    BA_AVG = pd.read_sql(
        'SELECT AVG(BA) FROM response_times',
        conn)
    LH_AVG = pd.read_sql(
        'SELECT AVG(LH) FROM response_times',
        conn)
    RA_AVG = pd.read_sql(
        'SELECT AVG(RA) FROM response_times',
        conn)
    print(KLM_AVG)
    print(BA_AVG)
    print(LH_AVG)
    print(RA_AVG)
    df = pd.DataFrame(data={'KLM' : 209.34, 'British Airways' : 683.87, 'Lufthansa' : 34.88, 'Ryan Air' : 519.77}, index=['Mean'])
    df

    def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                         header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                         bbox=[0, 0, 1, 1], header_columns=0,
                         ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)

        for k, cell in mpl_table._cells.items():
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])
        return ax.get_figure(), ax

    fig, ax = render_mpl_table(df, header_columns=0, col_width=4.0)
    fig.savefig('Plots\\tableResponse.png')

conn = sqlite3.connect('D:\\EXPORT\\ALL_DATA.sqlite')
cursor = conn.cursor()
exec(open('SQLITE_Queries.py').read())
cursor.executescript(QUERY_KLM_TWEETS)
cursor.executescript(QUERY_RESPONSE_TIME)
response_times(conn, cursor)
cursor.execute('DROP TABLE IF EXISTS response_times;')
conn.commit();

