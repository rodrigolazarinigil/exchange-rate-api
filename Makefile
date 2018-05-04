SHELL := /bin/bash

build:
	docker-compose -f docker-compose.yml build exchange-rate

env-up:
	docker-compose -f docker-compose.yml build exchange-rate-db
	docker-compose -f docker-compose.yml build exchange-rate
	docker-compose -f docker-compose.yml up -d