init:
	pip install -r requirements.txt

test:
	py.test tests

cov:
	py.test-3 --cov=./

verify:
	flake8 --exit-zero

.PHONY: init tests