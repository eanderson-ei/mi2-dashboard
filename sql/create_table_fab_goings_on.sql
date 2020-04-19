CREATE TABLE fab_goings_on (
    id            INTEGER NOT NULL
                          PRIMARY KEY,
    focal_area_id INTEGER NOT NULL,
    goings_on     TEXT,
    FOREIGN KEY (
        focal_area_id
    )
    REFERENCES focal_areas (id) 
);