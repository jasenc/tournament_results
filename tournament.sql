-- tournament.sql -- This file is used to configure the database required for
-- tournament.py to store data as well as retrieve the necessary data to
-- complete different functions. This file is designed for iteration based work.
-- Access PostgreSQL and use '\i tournament.sql' to execute this file and load
-- the database with all necessary tables.
--
-- Jasen Carroll
-- July 31st, 2015

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

-- Create a view for player standings by wins.
CREATE VIEW player_standings AS
     SELECT players.id,
            players.name,
            COUNT(matches1.winner) AS wins,
            COUNT(matches2.winner + matches2.loser) AS total_matches
       FROM players
       -- Left join to ensure values with wins = 0 are not hidden.
       LEFT JOIN matches AS matches1
         ON players.id = matches1.winner
       -- Left join to ensure values with total_matches = 0 are not hidden.
       LEFT JOIN matches AS matches2
         ON players.id = matches2.winner OR players.id = matches2.loser
      GROUP BY players.id
      ORDER BY wins DESC;

-- Create a view from player_standings with numbered rows.
CREATE VIEW standings AS
     SELECT row_number() over(ORDER BY wins DESC NULLS last) AS row_num,
            id,
            name
       FROM player_standings;

-- From standings create a view of only odd rows.
CREATE VIEW standings_odd AS
     SELECT row_number() over(ORDER BY row_num DESC NULLS last) AS row_num_odd,
            id,
            name
       FROM standings
      WHERE mod(row_num, 2) = 1;

-- From standings create a view of only even rows.
CREATE VIEW standings_even AS
     SELECT row_number() over(ORDER BY row_num DESC NULLS last) AS row_num_even,
            id,
            name
       FROM standings
      WHERE mod(row_num, 2) = 0;

-- Match odd rows with even rows to produce next player match.
CREATE VIEW player_matches AS
     SELECT standings_odd.id AS id_player1,
            standings_odd.name AS name_player1,
            standings_even.id AS id_player2,
            standings_even.name AS name_player2
       FROM standings_odd, standings_even
      WHERE standings_odd.row_num_odd = standings_even.row_num_even;
