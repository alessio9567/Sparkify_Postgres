import os
import glob
import psycopg2
import pandas as pd
import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Creates dataframe df from json song data

    - Loads song, artist dimension tables from df
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = [df.song_id.values[0],df.title.values[0],df.artist_id.values[0],int(df.year.values[0]),float(df.duration.values[0])]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = [df.artist_id.values[0], df.artist_name.values[0], df.artist_location.values[0], float(df.artist_latitude.values[0]), float(df.artist_longitude.values[0])]

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Creates dataframe df from json log data

    - Loads user,time dimension table and songplay fact table from df
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
   
    df['timestamp']=pd.to_datetime(df.ts,unit='ms')
    df['hour']=df.timestamp.dt.hour
    df['day']=df.timestamp.dt.day
    df['weekofyear']=df.timestamp.dt.weekofyear
    df['month']=df.timestamp.dt.month
    df['year']=df.timestamp.dt.year
    df['weekday']=df.timestamp.dt.weekday
    df.sort_values('timestamp')
    
    time_df = df.filter(['timestamp','hour','day','weekofyear','month','year','weekday'],axis=1)
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.filter(['userId','firstName','lastName','gender','level'],axis=1)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, {'song_title':row.song, 'duration':row.length , 'artist_name':row.artist})
        results = cur.fetchone()
        
        if results:
            songid, artistid = results[:2]
        else:
            songid, artistid = None, None
        
        # insert songplay record
        songplay_data = ( index,row.timestamp, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Executes func for each file in filepath
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it

    - Inserts data in song and artist table

    - Inserts data in user,time and songplay table

    - Finally, closes the connection.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()