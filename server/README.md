# REST API DOCUMENTATION

## General API Standards

Every response from our api will have an `ok` field whichindicates whether some sort of unexpected behavior has occured.

If `ok` is `true`, the request completed succesfully with a `200` status, and you can expect the payload to contain a `data` field with the appropriate information.

```
{
  "ok": true,
  "data": {...}
}
```

If `ok` is `false`, the request was not succesful. The response will ***not*** have a `200` status response and the `message` field will contain a description of what might have happened.

```
{
  "ok": false,
  "message": "apocalypse"
}
```

### RESOURCE `/`

#### GET `/`

This endpoint is a heartbeat which will respond with the following if everything is operating as expected.

```
{
  "ok": true,
  "hello": "world"
}
```

### RESOURCE `/slack-users`

#### GET `/slack-users`

This endpoint will return the list of Slack users belonging to the SCS Competitions.

Only username, name, and profile picture will be returned for the sake of privacy.

```
{
  "ok": true,
  "data": [
    {
      "username": "algorithm_god",
      "realname": "Algo McAlgoFace",
      "avatar": "https://cdn-link-here.doesnt-exist"
    },
    {
      "username": "1337_haxxorz",
      "realname": "Anon Ymous",
      "avatar": "https://cdn-link-here.doesnt-exist"
    }
  ]
}

```
### RESOURCE `/users`

#### GET `/users`

This endpoint will return the list of app users belonging to the SCS Competitions.

Only username, name, score, and team name will be returned for the sake of privacy.

```
{
  "ok": true,
  "data": [
    {
      "username": "algorithm_god",
      "name": "Algo McAlgoFace",
      "score": 0,
      team: "Best Team 2017"
    },
    {
      "username": "l33thaxx0r",
      "name": "Ada Lovelace",
      "score": 15000,
      team: ":+1:"
    },
  ]
}
```

```
### RESOURCE `/add_user`

#### POST `/add_user`

This endpoint will add a user to the app.

Example payload:
```
  {
    "username": "algo_dude",
    "name": "Best Human",
    "password": "dsnaiugfsahfsna42o532sa" # hashed
  }
```

```
{
  "ok": true,
  "data": "Succesfully added user algo_dude"
}
```
