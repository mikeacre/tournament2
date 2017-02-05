Swiss Pairing tournament, runs on a PSQL database utilizing psycopg2.

To run the program, load the files into your server.

in psql type "/i tournament.sql"

This will create the database and tables.

Utilize the following functions:

deleteMatches() will clear all matches from the matches table

deletePlayers() will clear all players

registerPlater(name) where name is the players name, will add a player into the
players table
