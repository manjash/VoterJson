DROP TABLE IF EXISTS poll CASCADE;
DROP TABLE IF EXISTS poll_votes CASCADE;
DROP TABLE IF EXISTS poll_choices CASCADE;

CREATE TABLE poll (
    id SERIAL PRIMARY KEY,
    poll_name TEXT UNIQUE NOT NULL
);

CREATE TABLE poll_choices (
    id SERIAL PRIMARY KEY ,
    choice_name TEXT NOT NULL,
    poll_id INTEGER NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll (id)
);

CREATE TABLE poll_votes (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL,
    choice_id INTEGER NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll (id),
    FOREIGN KEY (choice_id) REFERENCES poll_choices (id)
);