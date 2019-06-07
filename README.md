# Data Modeling with Postgres
_________
Sparkify, a startup, wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Their data is in a directory of JSON logs on user activity on the app and another directory with JSON metadata on the songs in their app.
The goal of this project is to create a Postgres databsae that allow analytics team to optimize queries on song play analysis.

## Data Modeling Structure
____________
The database structure uses Star Schema with following tables:
### Fact Table
1. **songplay**: records in log data associated with song plays i.e. records with page NextSong
 - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*
### Dimension Tables
2. **users**: users in the app
- *song_id, title, artist_id, year, duration*
3. **artists**: artists in music database
 - *artist_id, name, location, latitude, longitude*
4. **time**: timestamps of records in songplay broken down into specific units
 - *start_time, hour, day, week, month, year, weekday*
 
## How to Run
___________
1. run create_tables.py
2. run etl.py

## Files
____________
1. `test.ipynb` displays the first few rows of each table.

2. `create_tables.py` drops and creates tables.

3. `etl.ipynb` reads and processes a single file from song_data and log_data and loads the data into tables. This notebook contains detailed instructions on the ETL process for each of the tables.

4. `etl.py` reads and processes files from song_data and log_data and loads them into tables. 

5. `sql_queries.py` contains all sql queries, and is imported into the last three files above.

