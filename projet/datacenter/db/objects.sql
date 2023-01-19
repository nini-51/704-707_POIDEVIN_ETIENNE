DROP TABLE IF EXISTS objects;

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  object_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  warehouse_id INTEGER NOT NULL,
  deliver_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  gps TEXT NOT NULL
);
