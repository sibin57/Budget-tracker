DROP TABLE IF EXISTS budget;

CREATE TABLE IF NOT EXISTS budget (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT NOT NULL, 
    income      INTEGER,
    spending    INTEGER
);

