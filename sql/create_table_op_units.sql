CREATE TABLE op_units (
    id              INTEGER NOT NULL
                            PRIMARY KEY,
    workstream_id   INTEGER NOT NULL,
    output_no       TEXT,
    op_unit         TEXT,
    goings_on       TEXT,
    work_plan       TEXT,
    meeting_notes   TEXT,
    catalog         TEXT,
    status          TEXT,
    timeline        TEXT,
    complete_annual TEXT,
    notes           TEXT,
    covid_updates   TEXT,
    FOREIGN KEY (
        workstream_id
    )
    REFERENCES workstreams (id) 
);
