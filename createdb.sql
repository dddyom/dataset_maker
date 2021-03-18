create table datasets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,

    dataset_folder TEXT,

    targets TEXT,
    strays TEXT
);

CREATE TABLE matrices(
    name TEXT PRIMARY KEY,
    label TEXT,
    path TEXT,
    coordinates TEXT,
    value TEXT
);

create table chunks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT,
    count INTEGER,

    is_target BOOLEAN,

    width INTEGER,
    length INTEGER,

    mother_matrix TEXT,
    dataset TEXT,
    FOREIGN KEY (dataset) REFERENCES datasets(name)

    FOREIGN KEY(mother_matrix) REFERENCES matrixes(name)
);
