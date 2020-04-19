CREATE TABLE bva_tdy_approved (
    focal_area INTEGER,
    tdy        TEXT,
    approved   REAL,
    year       INTEGER,
    FOREIGN KEY (
        focal_area
    )
    REFERENCES bva_fa_bi (id) 
);