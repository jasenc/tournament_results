-- This file is designed for iteration based work.
-- Access PostgreSQL and use '\i tournament.sql' to execute this file and load
-- the database with all necessary tables.

-- Drop the current database named 'tournament'.
DROP DATABASE tournament;
-- If tournament database does not already exist comment out the above line.

-- Create a new database named 'tournament'.
CREATE DATABASE tournament;

-- Connect to tournament database.
\c tournament;

-- Create a table for players.
CREATE TABLE players (id SERIAL primary key,
                      name TEXT);

-- Create a table for matches.
CREATE TABLE matches (id SERIAL primary key,
                      winner INTEGER REFERENCES players (id),
                      loser INTEGER REFERENCES players (id));

CREATE VIEW player_standings AS
     SELECT players.id,
            players.name,
            COUNT(matches1.winner) AS wins,
            COUNT(matches2.winner + matches2.loser) AS total_matches
       FROM players
       -- Left join to ensure values with wins = 0 are not hidden
       LEFT JOIN matches AS matches1
         ON players.id = matches1.winner
       -- Left join to ensure values with total_matches = 0 are not hidden
       LEFT JOIN matches AS matches2
         ON players.id = matches2.winner OR players.id = matches2.loser
      GROUP BY players.id
      ORDER BY wins DESC;
