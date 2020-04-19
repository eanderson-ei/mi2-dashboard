CREATE TABLE bva_projects (
    id            INTEGER NOT NULL
                          PRIMARY KEY,
    focal_area_id INTEGER,
    project       TEXT,
    FOREIGN KEY (
        focal_area_id
    )
    REFERENCES bva_fa_bi (id) 
);