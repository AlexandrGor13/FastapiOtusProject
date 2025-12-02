.ONESHELL:

.PHONY: help
help: ## Вывод справки
	@egrep '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Установка проекта и pre-commit
	@uv sync --frozen --no-dev
	@uv run pre-commit autoupdate
	@uv run pre-commit install

.PHONY: up
up: ## Запуск контейнера
	@docker compose up -d --build

.PHONY: down
down: ## Остановка контейнера
	@docker compose down

.PHONY: bash
bash: ## Перейти в контейнер
	@docker compose exec app /bin/bash

.PHONY: pre-commit
pre-commit: ## Запуск pre-commit для всех файлов
	@pre-commit run --all-files --verbose || true

.PHONY: ps
ps: ## Просмотр информации о контейнере
	@docker compose ps

.PHONY: test
test: ## Запуск тестов
	@pytest test/

.PHONY: check
check: ## Запуск mypy
	@mypy  --ignore-missing-imports ./app

.PHONY: lint
lint: ## Запуск ruff
	@ruff check

