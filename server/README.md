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





