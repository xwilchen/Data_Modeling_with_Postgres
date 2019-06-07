import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process and extract data from a song file and insert data into songs and artists dimension tables.
    
    Parameters
    ----------
        cur : psycopg2.connect.cursor
            cursor from psycopg2 connecting to Postgres database.
        
        filepath: str
            The absolute filepath of a song file in string format.
    
    """
    df = pd.read_json(filepath, lines=True)

    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process and extract data from a log file and insert data into time and users dimension tables and songplay fact table.
    
    Parameters
    ----------
        cur : psycopg2.connect.cursor
            cursor from psycopg2 connecting to Postgres database.
        
        filepath: str
            The absolute filepath of a log file in string format.
    
    """
    df = pd.read_json(filepath, lines=True)

    df = df[df['page'] == 'NextSong']

    t = pd.to_datetime(df['ts'],unit='ms')
    
    time_data = (t, t.dt.hour.values.tolist(), t.dt.day.values.tolist(), t.dt.week.values.tolist(), t.dt.month.values.tolist(), t.dt.year.values.tolist(), t.dt.weekday.values.tolist())
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame({k:v for k, v in zip(column_labels, time_data)})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (pd.to_datetime(row.ts), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Process and extract data from a song file and insert data into songs and artists dimension tables.
    
    Parameters
    ----------
        cur : psycopg2.connect.cursor
            cursor from psycopg2 connecting to Postgres database.
        
        connect : psycopg2.connect
            connection to Postgres database.
        
        filepath: str
            The filepath of song and log files in string format.
            
        func: process_song_file or process_log_file
            specify process function.
    
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()