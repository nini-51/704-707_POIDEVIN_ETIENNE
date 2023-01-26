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
