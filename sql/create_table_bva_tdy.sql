CREATE TABLE bva_tdy (
    focal_area INTEGER,
    tdy        TEXT,
    period     [START TEXT],
    billed     REAL,
    FOREIGN KEY (
        focal_area
    )
    REFERENCES bva_fa_bi (id) 
);