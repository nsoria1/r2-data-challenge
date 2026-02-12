.PHONY: setup generate-data load transform test run docs docs-serve clean help

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
DBT = $(VENV)/bin/dbt

# Load environment variables from .env
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Default target
help:
	@echo "R2 Data Challenge - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Create venv and install dependencies"
	@echo ""
	@echo "Pipeline:"
	@echo "  make generate-data  - Generate sample test data"
	@echo "  make load           - Load CSV files to Snowflake"
	@echo "  make transform      - Run dbt transformations"
	@echo "  make run            - Run complete pipeline (load + transform)"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests (Python + dbt)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           - Generate dbt documentation"
	@echo "  make docs-serve     - Serve dbt docs at localhost:8080"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove generated data files"

# Setup
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

setup: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(DBT) deps --project-dir dbt_project --profiles-dir dbt_project
	@echo ""
	@echo "Setup complete! Don't forget to:"
	@echo "  1. Copy .env.example to .env and fill in your Snowflake credentials"
	@echo "  2. Run scripts/setup_snowflake.sql in Snowflake to create database/schemas"

# Data generation
generate-data:
	$(PYTHON) scripts/generate_sample_data.py --output-dir data/inbox

# Pipeline steps
load:
	PYTHONPATH=. $(PYTHON) src/loader.py --load-only

transform:
	$(DBT) run --project-dir dbt_project --profiles-dir dbt_project

# Full pipeline
run:
	PYTHONPATH=. $(PYTHON) src/loader.py

# Testing
test-python:
	$(PYTHON) -m pytest tests/ -v

test-dbt:
	$(DBT) test --project-dir dbt_project --profiles-dir dbt_project

test: test-python test-dbt

# Documentation
docs:
	$(DBT) docs generate --project-dir dbt_project --profiles-dir dbt_project
	@echo ""
	@echo "Documentation generated! To view, run:"
	@echo "  make docs-serve"

docs-serve:
	@echo "Starting dbt docs server at http://localhost:8080"
	$(DBT) docs serve --project-dir dbt_project --profiles-dir dbt_project --port 8080

# Cleanup
clean:
	rm -rf data/inbox/*.csv
	rm -rf data/processed/*.csv
	@echo "Cleaned data folders"
