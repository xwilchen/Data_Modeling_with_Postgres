# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

## FACT TABLE
songplay_table_create = ("""\
CREATE TABLE IF NOT EXISTS songplay \
(songplay_id SERIAL, \
start_time TIMESTAMP NOT NULL, \
user_id VARCHAR NOT NULL, \
level TEXT, \
song_id VARCHAR, \
artist_id VARCHAR, \
session_id INT, \
location VARCHAR, \
user_agent VARCHAR, \
PRIMARY KEY (songplay_id)) 
""")

## DIMENSION TABLES
user_table_create = ("""\
CREATE TABLE IF NOT EXISTS users \
(user_id VARCHAR NOT NULL UNIQUE, \
first_name VARCHAR, \
last_name VARCHAR, \
gender TEXT, \
level TEXT, \
PRIMARY KEY (user_id))
""")

song_table_create = ("""\
CREATE TABLE IF NOT EXISTS songs \
(song_id VARCHAR NOT NULL UNIQUE, \
title VARCHAR, \
artist_id VARCHAR, \
year INT, \
duration FLOAT, \
PRIMARY KEY (song_id))
""")

artist_table_create = ("""\
CREATE TABLE IF NOT EXISTS artists \
(artist_id VARCHAR NOT NULL UNIQUE, \
name VARCHAR, \
location VARCHAR, \
latitude FLOAT, \
longitude FLOAT, \
PRIMARY KEY (artist_id))
""")

time_table_create = ("""\
CREATE TABLE IF NOT EXISTS time \
(start_time TIMESTAMP NOT NULL UNIQUE, \
hour INT, \
day INT, \
week INT, \
month INT, \
year INT, \
weekday INT,\
PRIMARY KEY (start_time))
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay (start_time, user_id,level, song_id, artist_id, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (songplay_id) DO NOTHING""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (song_id) DO NOTHING""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (artist_id) DO NOTHING""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month , year , weekday) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (start_time) DO NOTHING""")

# FIND SONGS

song_select = ("""SELECT songs.song_id, artists.artist_id FROM songs JOIN artists ON songs.artist_id = artists.artist_id WHERE title = %s AND artists.name = %s AND songs.duration = %s""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
