setup:
	pip install --upgrade pip poetry
	poetry config virtualenvs.in-project true --local
	poetry install