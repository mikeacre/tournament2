#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def doExecute(sql, name=''):
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    if name != '':
        sql = sql, (name,)
    c.execute(sql)
    DB.commit()
    DB.close()
    return True;

def getOne(sql):
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute(sql)
    row =  c.fetchone()
    DB.commit()
    DB.close()
    return row;


def getAll(sql):
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute(sql)
    rows =  c.fetchall()
    DB.commit()
    DB.close()
    return rows

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    doExecute('DELETE FROM matches')


def deletePlayers():
    """Remove all the player records from the database."""
    doExecute('DELETE FROM contestants')


def countPlayers():
    """Returns the number of players currently registered."""
    numplayers = getOne('select count(*) from contestants')[0]
    return numplayers

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute(("insert into contestants (contestant) VALUES (%s)"), (name,))
    DB.commit()
    DB.close()
    return True



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql ="""
    SELECT contestants.id, contestants.contestant, count(matches.winner),
    (SELECT count(*) FROM matches WHERE contestants.id = matches.winner OR contestants.id = matches.loser) AS matches
    FROM contestants
    LEFT JOIN matches ON contestants.id = matches.winner
    GROUP BY contestants.id
    ORDER BY count(matches.winner) DESC
    """
    numplayers = getAll(sql)
    return numplayers


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("insert into matches (winner, loser) VALUES (%s,%s)", (winner,loser,))
    DB.commit()
    return True

def hasPlayed(player1,player2):
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute('select count(*) FROM matches WHERE (winner = %s AND loser = %s) OR (winner = %s AND loser = %s)', (player1,player2,player2,player1,))
    played = c.fetchone()[0]
    if played == 0:
        return False
    else:
        return True

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    matches = []

    while len(standings) > 1:
        player1 = standings.pop(0)
        i=0
        while hasPlayed(player1[0], standings[i][0]):
            i=i+1
        player2 = standings.pop(i)
        matches.append((player1[0],player1[1],player2[0],player2[1]))
    return matches

print countPlayers()
print playerStandings()
