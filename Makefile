SRC_DIR := ./supermarket_pricing
TEST_DIR := ./tests

setup:
	pip install --upgrade pip poetry
	poetry config virtualenvs.in-project true --local
	poetry install

fmt:
	poetry run black --config=pyproject.toml $(TEST_DIR) $(SRC_DIR)
	poetry run isort --settings-file=pyproject.toml $(TEST_DIR) $(SRC_DIR)

lint:
	poetry run flake8 --config=.flake8 $(SRC_DIR)
	poetry run black --config=pyproject.toml --check --diff $(SRC_DIR)
	poetry run isort --settings-file=pyproject.toml --check $(SRC_DIR)
	poetry run mypy --config=pyproject.toml $(SRC_DIR)

test:
	poetry run pytest -vv tests/