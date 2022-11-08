INSERT INTO poll (poll_name)
values
    ('pokemons'),
    ('animals');

INSERT INTO poll_choices (choice_name, poll_id)
values
    ('pikachu', 1),
    ('meuwt', 1),
    ('bulbasaur', 1),
    ('cat', 2),
    ('dog',  2),
    ('parrot', 2),
    ('hamster', 2);

INSERT INTO poll_votes (poll_id, choice_id)
values
    (1, 2),
    (1, 2),
    (1, 2),
    (1, 2),
    (1, 2),
    (1, 2),
    (1, 3),
    (1, 3),
    (1, 3),
    (1, 1),
    (1, 1),
    (1, 1),
    (1, 1),
    (1, 1),
    (1, 1),
    (2, 4),
    (2, 4),
    (2, 6),
    (2, 6),
    (2, 6),
    (2, 6),
    (2, 5),
    (2, 4),
    (2, 5),
    (2, 7),
    (2, 7),
    (2, 7),
    (2, 4),
    (2, 7),
    (2, 7);