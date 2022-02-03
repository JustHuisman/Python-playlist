# Python-playlist
A simple program which imports a file to make a playlist and insert it into the Chinook database

- Download the Chinook database file from https://www.sqlitetutorial.net/sqlite-sample-database/.
- Get a database program for SQlite, for example from https://sqlitebrowser.org/.
- Unzip the Chinook database file and put the chinook.db into the database program.
- Prepare a (text) file with keywords from songs you want to make a playlist for.
- Fill in the right path at the start of the code where you downloaded your Chinook database file.

# What it does
It will read out a file line by line and look for words in it that corresponds to track names from the database. 
If there are 0 tracks found on a line, it will display an error at the end of the program.
If there is 1 track found, it will be added to the playlist. 
If there are more tracks found, it will display a selection menu and then adding your choice to the playlist.
