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
           COUNT(matches.winner) AS wins,
           COUNT(matches.winner + matches.loser) AS total_matches
      FROM players
      LEFT JOIN matches
        ON players.id = matches.winner OR players.id = matches.loser
     GROUP BY players.id
     ORDER BY wins DESC;

CREATE VIEW total_loses AS
    SELECT players.id,
           players.name,
           COUNT(matches.loser) AS loses
      FROM players
      JOIN matches
        ON players.id = matches.loser
     GROUP BY players.id
     ORDER BY loses;
--
-- CREATE VIEW total_matches AS
--    SELECT players.id,
--           players.name,
--           COUNT(matches.winner + matches.loser) AS total_matches
--      FROM players
--      JOIN matches
--        ON players.id = matches.winner AND players.id = matches.loser
--     GROUP BY players.id
--     ORDER BY players.id;
--
-- CREATE VIEW player_standings AS
--     SELECT players.id,
--            players.name,
--            total_wins.wins,
--            total_matches.total_matches
--       FROM players, total_wins, total_matches
--      WHERE players.id = total_wins.id AND total_wins.id = total_matches.id;
