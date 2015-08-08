#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# Import pyscopg2 to utilize PostgreSQL with Python
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        c = db.cursor()
        return db, c
    except:
        print ("Could not connect to the database.")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    query = "TRUNCATE matches;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    query = "TRUNCATE players, matches;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    query = "SELECT COUNT(id) FROM players;"
    c.execute(query)
    # Used fetchone() because there should only be one result.
    count = c.fetchone()
    db.close()
    # fetchone() returns a tuple, here we need the first/only element.
    return int(count[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    # Avoid SQL injection by utilizing the second argument of execute().
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    c.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # count wins from matches return players.name order by wins DESC
    db, c = connect()
    query = "SELECT * FROM player_standings;"
    c.execute(query)
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    # Avoid SQL injection by utilizing the second argument of execute().
    query = "INSERT INTO matches (winner, loser) VALUES\
            ((SELECT id FROM players WHERE players.id=(%s)),\
            (SELECT id FROM players WHERE players.id=(%s)));"
    parameter = (winner, loser)
    c.execute(query, parameter)
    db.commit()
    db.close()


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
    # count = countPlayers()
    # standings = playerStandings()
    # pairings = []
    # i = 0
    # while i < count:
    #     match = [standings[i][0], standings[i][1],
    #              standings[i+1][0], standings[i+1][1]]
    #     pairings.append(match)
    #     i += 2
    # return pairings
    db, c = connect()
    query = "SELECT * FROM player_matches;"
    c.execute(query)
    player_matches = c.fetchall()
    db.close()
    return player_matches
