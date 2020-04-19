CREATE TABLE points_of_contact (
    people_id          INTEGER,
    workstream_product INTEGER,
    op_unit            INTEGER,
    FOREIGN KEY (
        people_id
    )
    REFERENCES people (id),
    FOREIGN KEY (
        workstream_product
    )
    REFERENCES workstream_products (id),
    FOREIGN KEY (
        op_unit
    )
    REFERENCES op_units (id) 
);
