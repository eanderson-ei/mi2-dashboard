CREATE TABLE workstream_products (
    id              INTEGER NOT NULL
                            PRIMARY KEY,
    workstream_id   INTEGER NOT NULL,
    product_no      TEXT,
    product_name    TEXT,
    what_to_track   TEXT,
    treatment       TEXT,
    senior_reviewer INTEGER,
    dec_submission  TEXT,
    link            TEXT,
    status          TEXT,
    timeline        TEXT,
    complete        TEXT,
    due             TEXT,
    notes           TEXT,
    FOREIGN KEY (
        workstream_id
    )
    REFERENCES workstreams (id),
    FOREIGN KEY (
        senior_reviewer
    )
    REFERENCES people (id) 
);
