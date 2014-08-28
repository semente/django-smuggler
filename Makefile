.PHONY: coverage tests lint

tests:
	python tests/run_tests.py

coverage:
	coverage run --source smuggler --branch tests/run_tests.py
	coverage report -m
	coverage html
	python -mwebbrowser htmlcov/index.html

lint:
	flake8 smuggler tests
