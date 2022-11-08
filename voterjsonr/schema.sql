DROP TABLE IF EXISTS poll;
DROP TABLE IF EXISTS poll_votes;
DROP TABLE IF EXISTS poll_choices;

CREATE TABLE poll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_name TEXT UNIQUE NOT NULL
);

CREATE TABLE poll_choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    choice_name TEXT NOT NULL,
    poll_id INTEGER NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll (id)
);

CREATE TABLE poll_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    choice_id INTEGER NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll (id),
    FOREIGN KEY (choice_id) REFERENCES poll_choices (id)
);