CREATE TABLE buy_in_tasks (
    id         INTEGER NOT NULL
                       PRIMARY KEY,
    buy_in_id  INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    task       TEXT,
    FOREIGN KEY (
        buy_in_id
    )
    REFERENCES buy_ins (id),
    FOREIGN KEY (
        product_id
    )
    REFERENCES buy_in_products (id) 
);
