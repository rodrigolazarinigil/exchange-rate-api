SHELL := /bin/bash

build:
	docker-compose -f docker-compose.yml build exchange-rate

drop-db:
	docker rm -f db

drop-app:
	docker rm -f app

start-db:
	docker-compose -f docker-compose.yml build db
	docker-compose -f docker-compose.yml -p  exchange-rate up -d db

start-app:
	docker-compose -f docker-compose.yml build app
	docker-compose -f docker-compose.yml -p exchange-rate up -d app

unit-tests:
	docker-compose -f docker-compose.yml build app
	docker-compose -f tests/docker-compose.yml build tests
	docker-compose -f tests/docker-compose.yml run --rm
	tests