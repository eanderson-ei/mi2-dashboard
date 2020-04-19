CREATE TABLE bva_loe_approved (
    project        INTEGER,
    staff          INTEGER,
    functional_cat TEXT,
    gsa_cat        TEXT,
    approved       REAL,
    year           INT,
    FOREIGN KEY (
        project
    )
    REFERENCES bva_projects (id),
    FOREIGN KEY (
        staff
    )
    REFERENCES people (id) 
);