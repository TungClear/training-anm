# Bank Account Project

## Prerequisite

- Docker 19+
- Docker Compose

## How to start

- Start the Docker stack by:

```sh
docker-compose up -d
```

- Pre-populate users for authentication for first time:

```sh
docker exec -it bank_account_api python manage.py seed_db
```

## Running Test

```sh
docker exec -it bank_account_api_test sh run_test.sh
```

## Open browser web

```sh
Access 127.0.0.1:3010 for opening swagger ui
```
```sh
Access 127.0.0.1:1234 for opening admin mongo
```
```sh
Access 127.0.0.1:5556 for opening app
```
```sh
Access 127.0.0.1:5555 for opening api
```
