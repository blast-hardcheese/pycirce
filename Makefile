test:
	python -m unittest discover -s ./tests/

lint:
	pylint $$(git ls-files '*.py')

format:
	black src tests
	