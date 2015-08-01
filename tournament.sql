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
