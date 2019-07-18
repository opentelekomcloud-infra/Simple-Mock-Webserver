### Simple Mock Server

This is single-purpose web server having 2 endpoints:

`/entities` — for listing all existing entities

`/entity`, `/entity/<uuid>` — for creating and retrieving existing entities

Server can use either `DEBUG` sqlite DB or postgresql database configured via environment variables:
 * `PG_DB_URL`
 * `PG_DATABASE`
 * `PG_USERNAME`
 * `PG_PASSWORD`

Debug mode is switched using `DEBUG` env variable and enabled by default