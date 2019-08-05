### Simple Mock Server

[![Build Status](https://travis-ci.com/opentelekomcloud-infra/Simple-Mock-Webserver.svg?branch=master)](https://travis-ci.com/outcatcher/Simple-Mock-Webserver)
![PyPI](https://img.shields.io/pypi/v/too-simple-server)

This is single-purpose web server having 2 endpoints:

`/entities` — for listing all existing entities

`/entity`, `/entity/<uuid>` — for creating and retrieving existing entities

Server can use either debug sqlite DB or PostgreSQL database

Server configuration is done with configuration yaml file:
```yaml
debug: true
server_port: 5449 

pg_bd_url: 'localhost:9999'
pg_database: 'users'
pg_username: 'admin'
pg_password: 'qwertyui!'
```

Default location of configuration file is `/etc/too-simple/config.yml`,
this can be changed using `--config` argument 

Debug mode is switched using `--debug` argument and enabled by default
