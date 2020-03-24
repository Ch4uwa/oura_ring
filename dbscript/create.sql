CREATE TABLE IF NOT EXISTS oura_data
(
    Timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP,
    Id            INT PRIMARY KEY,
    Name          TEXT,
    Personal_info json,
    Sleep         json,
    Activity      json,
    Readiness     json
);

CREATE TABLE IF NOT EXISTS oura_token
(
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Id        INT PRIMARY KEY,
    token     json
);