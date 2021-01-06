# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("create table songplays  (songplay_id serial NOT NULL PRIMARY KEY ,\
                                                   start_time timestamp NOT NULL,\
                                                   user_id int NOT NULL,\
                                                   level varchar NOT NULL,\
                                                   song_id varchar ,\
                                                   artist_id varchar ,\
                                                   session_id int NOT NULL,\
                                                   location varchar NOT NULL,\
                                                   user_agent varchar NOT NULL,\
                                                   CONSTRAINT fk_user \
                                                     FOREIGN KEY (user_id) \
                                                     REFERENCES users(user_id) \
                                                     ON DELETE SET NULL,\
                                                   CONSTRAINT fk_song \
                                                     FOREIGN KEY (song_id) \
                                                     REFERENCES songs(song_id) \
                                                     ON DELETE SET NULL,\
                                                   CONSTRAINT fk_artist \
                                                     FOREIGN KEY (artist_id) \
                                                     REFERENCES artists(artist_id) \
                                                     ON DELETE SET NULL)")

user_table_create = ("create table users (user_id int NOT NULL PRIMARY KEY,\
                                          first_name varchar ,\
                                          last_name varchar,\
                                          gender varchar,\
                                          level varchar)")

song_table_create = ("create table songs (song_id varchar NOT NULL PRIMARY KEY,\
                                          title varchar,\
                                          artist_id varchar,\
                                          year int,\
                                          duration numeric)")

artist_table_create = ("create table artists   (artist_id varchar NOT NULL PRIMARY KEY,\
                                                name varchar,\
                                                location varchar,\
                                                latitude numeric,\
                                                longitude numeric)")

time_table_create = ("create table time  (start_time timestamp NOT NULL,\
                                          hour int NOT NULL,\
                                          day int NOT NULL,\
                                          week int NOT NULL,\
                                          month int NOT NULL,\
                                          year int NOT NULL,\
                                          weekday int NOT NULL)")

# INSERT RECORDS

songplay_table_insert = ("insert into songplays values (%s,%s,%s,%s,%s,%s,%s,%s,%s) on conflict do nothing")

user_table_insert = ("insert into users values (%s,%s,%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level")

song_table_insert = ("insert  into songs values (%s,%s,%s,%s,%s) on conflict do nothing")

artist_table_insert = ("insert into artists values (%s,%s,%s,%s,%s) on conflict do nothing")

time_table_insert = ("insert into time values (%s,%s,%s,%s,%s,%s,%s)")

# FIND SONGS

song_select = ("select s.song_id,s.duration,s.artist_id \
                from songs s join artists a \
                on s.artist_id=a.artist_id \
                where s.title=%(song_title)s and s.duration=%(duration)s and a.name=%(artist_name)s")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]