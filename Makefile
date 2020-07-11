clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name __pycache__ -delete
	rm -f .coverage
	rm -rf htmlcov

lint:
	flake8 tests --config=tests/.flake8

test: clean lint
	pytest --rootdir=tests tests/

coverage: clean lint
	pytest --rootdir=tests --cov=serasa --cov-branch --cov-report=term --cov-report=html tests/