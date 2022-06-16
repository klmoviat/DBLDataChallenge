import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# niet super usefull meer omdat sentiment_year beter werkt
def avg_bar_plot(conn, cursor):
    df1 = pd.read_sql(
        "select AVG(head_sentiment) as opening_tweet, AVG(tail_sentiment) as last_tweet,"
        " AVG(delta_sentiment) as mean_difference, lang from KLM inner join main on head = id_str"
        " group by lang",
        conn)
    df1['Company_and_language'] = np.where(df1['lang'] == 'en', 'KLM English', 'KLM Dutch')
    df2 = pd.read_sql(
        "select AVG(head_sentiment) as opening_tweet, AVG(tail_sentiment) as last_tweet,"
        " AVG(delta_sentiment) as mean_difference, lang from British_Airways inner join main on head = id_str", conn)
    df2['Company_and_language'] = 'British Airways English'
    df3 = pd.read_sql(
        "select AVG(head_sentiment) as opening_tweet, AVG(tail_sentiment) as last_tweet,"
        " AVG(delta_sentiment) as mean_difference, lang from Lufthansa inner join main on head = id_str", conn)
    df3['Company_and_language'] = 'Lufthansa English'
    df4 = pd.read_sql(
        "select AVG(head_sentiment) as opening_tweet, AVG(tail_sentiment) as last_tweet,"
        " AVG(delta_sentiment) as mean_difference, lang from RyanAir inner join main on head = id_str", conn)
    df4['Company_and_language'] = 'RyanAir English'
    res = pd.concat([df1, df2, df3, df4])
    res.plot.bar(x='Company_and_language', rot=45)
    plt.ylabel('Average sentiment: 0 is fully negative, 1 is fully positive')
    plt.title('Average sentiment per company over the year')
    plt.tight_layout()
    plt.grid()
    plt.savefig("Plots\\AVG_bar.png", format='png')
    plt.show()


# instant
def violin_sentiment(conn, cursor):
    df1 = pd.read_sql(
        "select head_sentiment as opening_tweet, tail_sentiment as last_tweet,"
        " delta_sentiment from British_Airways",
        conn)

    df2 = pd.read_sql(
        "select head_sentiment as opening_tweet, tail_sentiment as last_tweet,"
        " delta_sentiment from KLM",
        conn)

    df3 = pd.read_sql(
        "select head_sentiment as opening_tweet, tail_sentiment as last_tweet,"
        " delta_sentiment from RyanAir",
        conn)

    df4 = pd.read_sql(
        "select head_sentiment as opening_tweet, tail_sentiment as last_tweet,"
        " delta_sentiment from Lufthansa",
        conn)

    fig = plt.figure(figsize=(12, 6), dpi=1200)
    gs = fig.add_gridspec(2, 6)

    ax = fig.add_subplot(gs[0, 0])
    sns.violinplot(data=df1['opening_tweet'], inner="quartile")
    ax.set_xlabel("opening_tweet")

    ax = fig.add_subplot(gs[0, 1])
    sns.violinplot(data=df1['last_tweet'], inner="quartile")
    ax.set_xlabel("last_tweet")
    ax.set_title('British Airways')
    ax = fig.add_subplot(gs[0, 2])
    sns.violinplot(data=df1['delta_sentiment'], inner="quartile")
    ax.set_xlabel("delta_sentiment")

    ax = fig.add_subplot(gs[0, 3])
    sns.violinplot(data=df2['opening_tweet'], color='darkorange', inner="quartile")
    ax.set_xlabel("opening_tweet")

    ax = fig.add_subplot(gs[0, 4])
    sns.violinplot(data=df2['last_tweet'], color='darkorange', inner="quartile")
    ax.set_xlabel("last_tweet")
    ax.set_title('KLM')

    ax = fig.add_subplot(gs[0, 5])
    sns.violinplot(data=df2['delta_sentiment'], color='darkorange', inner="quartile")
    ax.set_xlabel("delta_sentiment")

    ax = fig.add_subplot(gs[1, 0])
    sns.violinplot(data=df2['opening_tweet'], color='gold', inner="quartile")
    ax.set_xlabel("opening_tweet")

    ax = fig.add_subplot(gs[1, 1])
    sns.violinplot(data=df3['last_tweet'], color='gold', inner="quartile")
    ax.set_xlabel("last_tweet")
    ax.set_title('RyanAir')
    ax = fig.add_subplot(gs[1, 2])
    sns.violinplot(data=df3['delta_sentiment'], color='gold', inner="quartile")
    ax.set_xlabel("delta_sentiment")
    ax = fig.add_subplot(gs[1, 3])
    sns.violinplot(data=df4['opening_tweet'], color='forestgreen', inner="quartile")
    ax.set_xlabel("opening_tweet")

    ax = fig.add_subplot(gs[1, 4])
    sns.violinplot(data=df4['last_tweet'], color='forestgreen', inner="quartile")
    ax.set_xlabel("last_tweet")
    ax.set_title('Lufthansa')
    ax = fig.add_subplot(gs[1, 5])
    sns.violinplot(data=df4['delta_sentiment'], color='forestgreen', inner="quartile")
    ax.set_xlabel("delta_sentiment")
    plt.suptitle('Distribution of sentiment in conversations for 4 airlines')
    fig.tight_layout()
    plt.savefig("Plots\\violin.png", format='png')


# instant
def bar_box_count(conn, cursor):
    # queries to get number of conversations
    length_KLM = cursor.execute("""SELECT COUNT() FROM KLM """).fetchone()[0]
    length_BA = cursor.execute("""SELECT COUNT() FROM British_Airways""").fetchone()[0]
    length_LH = cursor.execute("""SELECT COUNT() FROM Lufthansa""").fetchone()[0]
    length_RA = cursor.execute("""SELECT COUNT() FROM RyanAir""").fetchone()[0]

    #Data for boxplot: depth of conversations
    depthklmtemp = cursor.execute("""SELECT depth FROM KLM""").fetchall()
    depthBAtemp = cursor.execute("""SELECT depth FROM main.British_Airways""").fetchall()
    depthLHtemp = cursor.execute("""SELECT depth FROM main.Lufthansa""").fetchall()
    depthRAtemp = cursor.execute("""SELECT depth FROM main.RyanAir""").fetchall()

    depthklm = [i[0]+1 for i in depthklmtemp]
    depthBA = [i[0]+1 for i in depthBAtemp]
    depthLH = [i[0]+1 for i in depthLHtemp]
    depthRA = [i[0]+1 for i in depthRAtemp]

    example_data = [depthklm, depthBA, depthLH, depthRA]
    data_len = [len(i) for i in example_data]
    labels = ['KLM', 'British Airways', 'Lufthansa', 'Ryanair']

    #make the plot
    fig, ax = plt.subplots()
    fig.figure(dpi=1200)
    ax.bar(range(1, len(data_len)+1), [length_KLM, length_BA, length_LH, length_RA], color='lightblue', align='center')
    ax2 = ax.twinx()
    ax2.boxplot(example_data)
    ax2.set_ylim(0, 15)
    ax.set_xticklabels(labels) # , rotation='vertical')
    plt.savefig("Plots\\bar_box_count.png", format='png')
    plt.show()


# approximately 45 seconds
def sentiment_year(conn, cursor):
    if 1:
        df1 = pd.read_sql("select created_at, sentiment from main where user_mentions like '%KLM%' "
                          "AND sentiment is not NULL "
                          "union select main.created_at, head_sentiment from KLM inner join main on id_str = head", conn)
        df1['created_at'] = pd.to_datetime(df1['created_at'])
        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=1200)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sentiment (0 is negative, 1 is positive)')
        df1 = df1.rename(columns={"created_at": "Date"})
        df1.groupby([df1['Date'].dt.date])['sentiment'].mean().plot(kind='line')
        plt.xticks(rotation=45)
        ax1.axhline(y=df1['sentiment'].mean(), linestyle='dashed', color='tab:blue')
        ax2 = ax1.twinx()
        ax1.set_ylim([0.2, 0.8])
        ax2.set_ylim([0, 5500])
        color = 'tab:red'
        ax2.set_ylabel('Number of tweets in the week', color=color)
        df1.groupby([df1['Date'].dt.date])['sentiment'].count().plot.area(alpha=0.2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b-'%y"))
        plt.title("Average sentiment and opening tweets per day for KLM (NOTE: follow-up tweets not included)")
        plt.tight_layout()
        plt.savefig("Plots\\sentiment_year_KLM.png", format='png')
        plt.show()
    if 1:
        df2 = pd.read_sql("select created_at, sentiment from main where user_mentions like '%British_Airways%' "
                          "AND sentiment is not NULL "
                          "union select main.created_at, head_sentiment from main.British_Airways"
                          " inner join main on id_str = head", conn)
        df2['created_at'] = pd.to_datetime(df2['created_at'])
        df2 = df2.rename(columns={"created_at": "Date"})
        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=1200)
        ax1.set_ylabel('Sentiment (0 is negative, 1 is positive)')
        df2.groupby([df2['Date'].dt.date])['sentiment'].mean().plot(kind='line')
        plt.xticks(rotation=45)
        ax1.axhline(y=df2['sentiment'].mean(), linestyle='dashed', color='tab:blue')
        ax2 = ax1.twinx()
        ax1.set_ylim([0.2, 0.8])
        ax2.set_ylim([0, 5500])
        color = 'tab:red'
        ax2.set_ylabel('Number of tweets in the week', color=color)
        df2.groupby([df2['Date'].dt.date])['sentiment'].count().plot.area(alpha=0.2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b-'%y"))
        plt.title("Average sentiment and opening tweets per day for British Airways (NOTE: follow-up tweets not included)")
        plt.tight_layout()
        plt.savefig("Plots\\sentiment_year_BA.png", format='png')
        plt.show()
    if 1:
        df3 = pd.read_sql("select created_at, sentiment from main where user_mentions like '%RyanAir%' "
                          "AND sentiment is not NULL "
                          "union select main.created_at, head_sentiment from RyanAir inner join main on id_str = head", conn)
        df3['created_at'] = pd.to_datetime(df3['created_at'])
        df3 = df3.rename(columns={"created_at": "Date"})
        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=1200)
        ax1.set_ylabel('Sentiment (0 is negative, 1 is positive)')
        df3.groupby([df3['Date'].dt.date])['sentiment'].mean().plot(kind='line')
        plt.xticks(rotation=45)
        ax1.axhline(y=df3['sentiment'].mean(), linestyle='dashed', color='tab:blue')
        ax2 = ax1.twinx()
        ax1.set_ylim([0.2, 0.8])
        ax2.set_ylim([0, 5500])
        color = 'tab:red'
        ax2.set_ylabel('Number of tweets in the week', color=color)
        df3.groupby([df3['Date'].dt.date])['sentiment'].count().plot.area(alpha=0.2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b-'%y"))
        plt.title("Average sentiment and opening tweets per day for RyanAir (NOTE: follow-up tweets not included)")
        plt.tight_layout()
        plt.savefig("Plots\\sentiment_year_RyanAir.png", format='png')
        plt.show()
    if 1:
        df4 = pd.read_sql("select created_at, sentiment from main where user_mentions like '%Lufthansa%' "
                          "AND sentiment is not NULL "
                          "union select main.created_at, head_sentiment from main.Lufthansa"
                          " inner join main on id_str = head", conn)
        df4['created_at'] = pd.to_datetime(df4['created_at'])
        df4 = df4.rename(columns={"created_at": "Date"})
        fig, ax1 = plt.subplots(figsize=(16, 8), dpi=1200)
        ax1.set_ylabel('Sentiment (0 is negative, 1 is positive)')
        df4.groupby([df4['Date'].dt.date])['sentiment'].mean().plot(kind='line')
        plt.xticks(rotation=45)
        ax1.axhline(y=df4['sentiment'].mean(), linestyle='dashed', color='tab:blue')
        ax2 = ax1.twinx()
        ax1.set_ylim([0.2, 0.8])
        ax2.set_ylim([0, 5500])
        color = 'tab:red'
        ax2.set_ylabel('Number of tweets in the week', color=color)
        df4.groupby([df4['Date'].dt.date])['sentiment'].count().plot.area(alpha=0.2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b-'%y"))
        plt.title("Average sentiment and opening tweets per day for Lufthansa (NOTE: follow-up tweets not included)")
        plt.tight_layout()
        plt.savefig("Plots\\sentiment_year_Luft.png", format='png')
        plt.show()
