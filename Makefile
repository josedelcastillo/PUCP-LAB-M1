PYTHON ?= $(shell command -v python3.12 || command -v python3)
VENV ?= .venv
BIN := $(VENV)/bin
IMAGE ?= pucp-lab-m1

.PHONY: install test lint run docker-build site

$(BIN)/python:
	$(PYTHON) -m venv $(VENV)

install: $(BIN)/python
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	$(BIN)/pip install -r requirements-dev.txt

test:
	$(BIN)/pytest --cov=app --cov-report=term-missing

lint:
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

run:
	$(BIN)/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t $(IMAGE):dev .

site:
	$(BIN)/python scripts/build_site.py --version dev --env local
