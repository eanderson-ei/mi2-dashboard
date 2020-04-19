CREATE TABLE buy_ins (
    id              INTEGER NOT NULL
                            PRIMARY KEY,
    buy_in          TEXT,
    goings_on       TEXT,
    work_plan       TEXT,
    manager         TEXT,
    timeline        TEXT,
    complete_lop    TEXT,
    complete_annual TEXT
);
