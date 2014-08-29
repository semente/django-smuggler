.PHONY: coverage tests lint

tests:
	python manage.py test

coverage:
	coverage run --source smuggler --branch manage.py test
	coverage report -m
	coverage html
	python -mwebbrowser htmlcov/index.html

lint:
	flake8 smuggler tests
