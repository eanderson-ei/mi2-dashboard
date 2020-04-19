CREATE TABLE buy_in_products (
    id             INTEGER NOT NULL
                           PRIMARY KEY,
    buy_in_id      INTEGER NOT NULL,
    product        TEXT,
    cor            TEXT,
    link           TEXT,
    product_status TEXT,
    timeline       TEXT,
    complete       TEXT,
    due            TEXT,
    notes          TEXT,
    FOREIGN KEY (
        buy_in_id
    )
    REFERENCES buy_ins (id) 
);