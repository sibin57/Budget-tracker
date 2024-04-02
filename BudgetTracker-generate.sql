DROP TABLE IF EXISTS budget;

CREATE TABLE IF NOT EXISTS budget (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    day         TEXT NOT NULL, 
    income      INTEGER,
    spending    INTEGER
);


