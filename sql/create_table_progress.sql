CREATE TABLE progress (
    quarter               TEXT,
    notes                 TEXT,
    workstream_product_id INTEGER,
    FOREIGN KEY (
        workstream_product_id
    )
    REFERENCES workstream_products (id) 
);
