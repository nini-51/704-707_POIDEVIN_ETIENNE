-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS packages;
DROP TABLE IF EXISTS archives;

CREATE TABLE packages (
  package_id TEXT UNIQUE PRIMARY KEY NOT NULL,
  status TEXT NOT NULL,
  warehouses TEXT NOT NULL,
  deliver_id TEXT,
  last_location TEXT NOT NULL
);

CREATE TABLE archives (
  package_id TEXT UNIQUE PRIMARY KEY NOT NULL,
  status TEXT NOT NULL,
  warehouses TEXT NOT NULL,
  deliver_id TEXT,
  last_location TEXT NOT NULL
);

-- Example

-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;
--
-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL
-- );
--
-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );
