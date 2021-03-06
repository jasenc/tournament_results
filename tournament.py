#!/usr/bin/env python
#
# tournament.py -- This program was written in order to maintain a Swiss
# pairings style tournament utilizing a database.
#
# Jasen Carroll
# July 31st, 2015

# Import pyscopg2 to utilize PostgreSQL with Python
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        # Connect to the database
        db = psycopg2.connect("dbname=tournament")
        # Create a cursor for the database
        c = db.cursor()
        # Returm the cursor and database
        return db, c
    except:
        # If the above does not work:
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


def countActivePlayers():
    """Returns the number of active players for the next match."""
    db, c = connect()
    query = "SELECT COUNT(id) FROM active_players;"
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

    try:
        db, c = connect()
        # Avoid SQL injection by utilizing the second argument of execute().
        query = "INSERT INTO matches (player_a, player_b, winner, loser) VALUES\
                ((SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)));"
        parameter = (winner, loser, winner, loser)
        c.execute(query, parameter)
        db.commit()
        db.close()
    except psycopg2.Error:
        db, c = connect()
        query = "INSERT INTO matches (player_a, player_b, winner, loser) VALUES\
                ((SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)),\
                (SELECT id FROM players WHERE players.id=(%s)));"
        parameter = (loser, winner, winner, loser)
        c.execute(query, parameter)
        db.commit()
        db.close()


def preventRematches(player_matches, previous_matches):
    """ This function is utilized by the following swissPairings().

    It is called by swissPairings() and is provided with the proposed
    player_matches as well as the previous_matches that have taken place
    during the tournamnet. With this information, preventRematches()
    recursively verifies there are no remaining rematches throughout the
    proposed matches.

    Args:
        player_matches: proposed matches from database, obtained in
                        swissPairings().
        previous_matches: previous matches from the duration of the tournament,
                          obtained in swissPairings().

    Returns:
        player_matches: the same tuple that is provided is then returned after
                        it is insured there are no rematches.
    """
    # Check to prevent rematches.
    # For every match returned from the database,
    for i in range(len(player_matches)):
        # and every match that has already occured,
        for j in range(len(previous_matches)):
            # check if that new match is the same as a previous match.
            if (player_matches[i][0] == previous_matches[j][0] and
               player_matches[i][2] == previous_matches[j][1]):

                # If it is, convert our new tuple to a list.
                player_matches = list(player_matches)
                # Then convert that particular tuple to a list.
                player_matches[i] = list(player_matches[i])
                # Record the player in the first position.
                this_player = player_matches[i][0]  # record this player

                # Try swapping them with the first player from the next match.
                try:
                    other_player = player_matches[i+1][0]
                    player_matches[i][0] = other_player
                    # Then we need to convert the following match to a list.
                    player_matches[i+1] = list(player_matches[i+1])
                    player_matches[i+1][0] = this_player
                    player_matches[i+1] = tuple(player_matches[i+1])
                # If there is an IndexError, swap with the first player from
                # the previous match.
                except IndexError:  # if there is an out of index error
                    other_player = player_matches[i-1][0]
                    player_matches[i][0] = other_player
                    player_matches[i-1] = list(player_matches[i-1])
                    player_matches[i-1][0] = this_player
                    player_matches[i-1] = tuple(player_matches[i-1])
                player_matches[i] = tuple(player_matches[i])
                player_matches = tuple(player_matches)

                return preventRematches(player_matches, previous_matches)

    return player_matches


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

    # Use the database to generate a tuple of proposed matches.
    db, c = connect()
    query = "SELECT * FROM player_matches;"
    c.execute(query)
    player_matches = c.fetchall()
    # Then use the database to generate a tuple of previous matches.
    query = "SELECT * FROM previous_matches;"
    c.execute(query)
    previous_matches = c.fetchall()
    db.close()
    # Provide these tuples to the previously defined preventRematches, and
    # assign its results as next_matches to be returned by this function.
    next_matches = preventRematches(player_matches, previous_matches)

    return next_matches
