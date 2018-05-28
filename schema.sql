CREATE TABLE user
(
  id INTEGER PRIMARY KEY,
  fullname VARCHAR(128),
  email VARCHAR(128) UNIQUE,
  password VARCHAR(128),
  validate_hash VARCHAR(128),
  is_validated INTEGER DEFAULT 0
);

CREATE TABLE gde
(
  id INTEGER PRIMARY KEY,
  name VARCHAR(128),
  path VARCHAR(128)
);