-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;


CREATE DATABASE tournament;

\connect tournament;

CREATE SEQUENCE user_id_seq;

CREATE TABLE contestants(
  ID INT                  PRIMARY KEY NOT NULL DEFAULT nextval('user_id_seq'),
  contestant VARCHAR (20) NOT NULL
);

CREATE TABLE matches(
  ID INT         PRIMARY KEY NOT NULL DEFAULT nextval('user_id_seq'),
  winner INT     NOT NULL REFERENCES contestants (ID),
  loser INT      NOT NULL REFERENCES contestants (ID)
);
