CREATE TABLE action_plans (
    id                 NOT NULL
                       PRIMARY KEY,
    workstream_id      NOT NULL,
    action_plan   TEXT,
    FOREIGN KEY (
        workstream_id
    )
    REFERENCES workstreams (id) 
);