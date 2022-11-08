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
{"poll_name": "animals", "choices": ['wolf', 'fox', 'sheep']}
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
