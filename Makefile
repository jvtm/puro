PY_DIRS := puro tests
PYTHON ?= python3.6

tox:
	tox

check: check-static unit-test

unit-test:
	$(PYTHON) -m pytest -vv -rs $(PY_DIRS)

check-static: check-flake8 check-pylint

check-flake8:
	$(PYTHON) -m flake8 --version
	$(PYTHON) -m flake8 $(PY_DIRS)

check-pylint:
	$(PYTHON) -m pylint --version
	$(PYTHON) -m pylint $(PY_DIRS)

check-format:
	autoflake --recursive --remove-unused-variables $(PY_DIRS)
	autopep8 --diff --recursive --experimental --aggressive --max-line-length=120 $(PY_DIRS)
	isort --diff --recursive $(PY_DIRS)

clean: clean-tox

clean-tox:
	rm -rvf .tox

