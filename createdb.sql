create table datasets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,

    targets TEXT,
    strays TEXT,
    train TEXT,
    test TEXT,

    main TEXT

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

    is_target BOOLEAN,
    origin BOOLEAN,

    width INTEGER,
    length INTEGER,

    azimuth INTEGER,
    distance INTEGER,

    mother_matrix TEXT,
    dataset TEXT,
    FOREIGN KEY (dataset) REFERENCES datasets(name)

    FOREIGN KEY(mother_matrix) REFERENCES matrixes(name)
);
