# -*- coding: utf-8 -*-
import sqlite3


def create_database():
    conn = sqlite3.connect('proverbaro.db')
    print 'Proverbaro database created'
    with conn:
        conn.execute('DROP TABLE if exists Proverbs')
        conn.execute(
            'CREATE TABLE Proverbs(id INTEGER PRIMARY KEY, text TEXT,'
            'shown_times INTEGER DEFAULT 0,'
            'shown_last_time TEXT DEFAULT null)')
        with open('output.txt', 'r') as proverbs_file:
            for proverb in proverbs_file:
                conn.execute(
                    'INSERT INTO Proverbs(text) VALUES (\'%s\');'
                    % proverb.replace('\'', '\'\''))

        conn.execute('DROP TABLE if exists Post_Ids')
        conn.execute(
            'CREATE TABLE Post_Ids(id INTEGER PRIMARY KEY, '
            'publish_date TEXT NOT NULL, '
            'publish_id INTEGER NOT NULL, '
            'proverb_id INTEGER NOT NULL REFERENCES Proverbs (id))')


if __name__ == '__main__':
    create_database()
