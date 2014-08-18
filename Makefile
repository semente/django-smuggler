.PHONY: coverage

coverage:
	coverage run --source smuggler tests/run_tests.py
	coverage report -m
	coverage html
	python -mwebbrowser htmlcov/index.html
