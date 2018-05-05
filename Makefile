SHELL := /bin/bash

build:
	docker-compose -f docker-compose.yml build exchange-rate

drop-db:
	docker rm -f db

start-db:
	docker-compose -f docker-compose.yml build db
	docker-compose -f docker-compose.yml -p exchange-rate up -d db

env-up:
	docker-compose -f docker-compose.yml build exchange-rate-db
	docker-compose -f docker-compose.yml build exchange-rate
	docker-compose -f docker-compose.yml up -d