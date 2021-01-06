

SPARKIFY ANALYTICS

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. 
Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app,
as well as a directory with JSON metadata on the songs in their app.

"create_tables.py" creates the fact table songplay which contains users activities and dimension tables time,users,song and artist
"etl.py" insert log and song data from JSON files into this tables

Description of schema database:

Fact Table:
songplays - records in log data associated with song plays i.e. records with page NextSong

Dimension Tables:
users - users in the app
songs - songs in music database
artists - artists in music database
time - timestamps of records in songplays broken down into specific units
