CREATE TABLE x_bva_tracker (
    bva_fa_bi  INTEGER,
    focal_area INTEGER,
    buy_in     INTEGER,
    FOREIGN KEY (
        bva_fa_bi
    )
    REFERENCES bva_fa_bi (id),
    FOREIGN KEY (
        focal_area
    )
    REFERENCES focal_areas (id),
    FOREIGN KEY (
        buy_in
    )
    REFERENCES buy_ins (id) 
);
