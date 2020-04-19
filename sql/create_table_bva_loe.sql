CREATE TABLE bva_loe (
    project      INTEGER,
    staff        INTEGER,
    period_start TEXT,
    billed       REAL,
    FOREIGN KEY (
        project
    )
    REFERENCES bva_projects (id),
    FOREIGN KEY (
        staff
    )
    REFERENCES people (id) 
);
