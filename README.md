# VoterJson
Trialing working on a production-like project (with tests, docker, CI etc) 


The project main logic can be found in [voterjsonr](https://github.com/manjash/VoterJson/tree/main/voterjsonr) folder.

Supported functionality:

- Creating a new poll
- Voting for a poll option
- Getting results of the existing polls

## Creating a new poll
Make a POST a json-format request to `/api/createPoll/` with the `poll_name` and `choices` options:

```
{"poll_name": "animals", "choices": ["wolf", "fox", "sheep"]}
```

## Voting for a poll option

Make a POST a json-format request to `/api/poll/` with `poll_id` and the `choice_id`:

```
{"poll_id": 1, "choice_id": 2}
```

## Getting results of the existing polls

Make a POST a json-format request to `/api/getResult/` with the `poll_id` of the poll:

```
{"poll_id": 1}
```


# Docker

Do this all inside venv. Venv is initiated through Dockerfile.

## Creating a container with postgres

For some reason, creating Dockerfile in /database and building -> running it didn't work.
That's why doing this instead:

First of all, launch Docker app locally. Then run

```
docker run --name voterjson_db -e POSTGRES_PASSWORD=qwerty123 -d postgres
```

Change to ```postgres``` user to access the DB

```
su postgres
```

Check the DB --> ```psql```

Check connection info --> ```\conninfo```

Exit interactive mode --> ```\q``` --> ```exit``` --> ```exit```

Check that docker is still running --> ```docker ps```

Stop / rm the container ```docker stop voterjson_db``` --> ```docker rm voterjson_db```

Run the container connected to PgAdmin to create a 'prod' postgres DB:
```docker run --name voterjson_db -p 5433:5432 -e POSTGRES_PASSWORD=qwerty123 -d postgres```

### And then create a test DB in the same container

```
psql -p 5433 -h localhost -U postgres -e POSTGRES_PASSWORD=qwerty123
create database voterjson_db_test
```



Good instructions on how to set up connections:
https://www.optimadata.nl/blogs/1/n8dyr5-how-to-run-postgres-on-docker-part-1

## Building/running docker with python

Everytime when something changes in the app, rebuild and then run

Locally:
```
docker build . -t voterjson
```

With docker compose:

```
docker compose up --build -d
```

### Running Docker

```
docker run --rm -it -p 5001:5001 voterjson
```

## For debugging

To see folders and files

```
docker run --rm -it voterjson bash
```

## Code check with linter

Locally:
```
pylint $(git ls-files '*.py')
```

With docker compose:
```
docker compose exec app pylint $(git ls-files '*.py')
```

## Pytest test runs

### Running tests locally:

Before running tests, make sure that the DB `voterjson_db_test` is created. If not, repeat [these steps](#And-then-create-a-test-DB-in-the-same-container).

The command below takes params from .env.testing and feeds them directly into pytest

```
env $(cat .env.testing) pytest
```

### Running tests with docker compose

```
docker compose exec app pytest
```
