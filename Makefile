SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: help up down build logs migrate seed test clean ps frontend-install smoke validate

help:
	@echo "AstraCart Enterprise Platform"
	@echo "  make up       - build and start all services"
	@echo "  make down     - stop services"
	@echo "  make build    - docker compose build"
	@echo "  make logs     - stream service logs"
	@echo "  make migrate  - run Alembic migrations in every service"
	@echo "  make seed     - seed all service databases"
	@echo "  make test     - run backend and gateway tests"
	@echo "  make validate - run repository structural validation"
	@echo "  make clean    - remove containers, volumes and caches"

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

migrate:
	bash scripts/migrate.sh

seed:
	bash scripts/seed.sh

test:
	bash scripts/test.sh

validate:
	python scripts/validate_project.py

clean:
	docker compose down -v --remove-orphans
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name node_modules -prune -exec rm -rf {} +
