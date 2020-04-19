CREATE TABLE workstreams (
    id            INTEGER NOT NULL
                          PRIMARY KEY,
    focal_area_id INTEGER NOT NULL,
    goings_on_id  INTEGER NOT NULL,
    workstream    TEXT,
    FOREIGN KEY (
        focal_area_id
    )
    REFERENCES focal_areas (id),
    FOREIGN KEY (
        goings_on_id
    )
    REFERENCES fab_goings_on (id) 
);
