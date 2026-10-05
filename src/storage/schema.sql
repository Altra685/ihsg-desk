-- IHSG Desk — skema basis data

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS tickers (
    code       TEXT PRIMARY KEY,
    name       TEXT,
    sector     TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS prices (
    code   TEXT NOT NULL,
    date   TEXT NOT NULL,
    open   REAL,
    high   REAL,
    low    REAL,
    close  REAL,
    volume REAL,
    PRIMARY KEY (code, date)
);

CREATE INDEX IF NOT EXISTS idx_prices_code_date ON prices (code, date);