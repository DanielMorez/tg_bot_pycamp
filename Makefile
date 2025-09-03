.PHONY: help install install-dev test lint format check clean run docker-build docker-run

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

install-dev: ## Установить зависимости для разработки
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Запустить тесты
	pytest

test-cov: ## Запустить тесты с покрытием
	pytest --cov=src --cov-report=html --cov-report=term-missing

lint: ## Проверить код с помощью Ruff
	ruff check src/ tests/

lint-fix: ## Исправить проблемы с кодом
	ruff check --fix src/ tests/

format: ## Отформатировать код
	ruff format src/ tests/

check: ## Проверить типы с помощью MyPy
	mypy src/

check-all: lint format check ## Запустить все проверки

clean: ## Очистить кеш и временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage

run: ## Запустить бота
	python bot.py

docker-build: ## Собрать Docker образ
	docker-compose build

docker-run: ## Запустить с помощью Docker
	docker-compose up -d

docker-logs: ## Показать логи Docker
	docker-compose logs -f

docker-stop: ## Остановить Docker контейнеры
	docker-compose down

docker-clean: ## Очистить Docker контейнеры и образы
	docker-compose down -v --rmi all
