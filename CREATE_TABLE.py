import json
import glob
import numpy as np
import pandas as pd
import csv, sqlite3

conn = sqlite3.connect("DataChallenge.sqlite")
cursor = conn.cursor()

#NOTE: unneccesasary want to_sql doet het zelf blijkbaar


cursor.execute('''CREATE TABLE temp
(
    created_at                TEXT,
    id                        REAL,
    id_str                    REAL,
    text                      TEXT,
    display_text_range        TEXT,
    source                    TEXT,
    truncated                 REAL,
    in_reply_to_status_id     REAL,
    in_reply_to_status_id_str REAL,
    in_reply_to_user_id       REAL,
    in_reply_to_user_id_str   REAL,
    in_reply_to_screen_name   TEXT,
    user                      TEXT,
    geo                       TEXT,
    coordinates               TEXT,
    place                     TEXT,
    contributors              TEXT,
    is_quote_status           REAL,
    quote_count               REAL,
    reply_count               REAL,
    retweet_count             REAL,
    favorite_count            REAL,
    entities                  TEXT,
    extended_entities         TEXT,
    favorited                 REAL,
    retweeted                 REAL,
    possibly_sensitive        REAL,
    filter_level              TEXT,
    lang                      TEXT,
    timestamp_ms              TEXT,
    retweeted_status          TEXT,
    extended_tweet            TEXT,
    quoted_status_id          TEXT,
    quoted_status_id_str      TEXT,
    quoted_status             TEXT,
    quoted_status_permalink   TEXT,
    "delete"                  TEXT
)''')