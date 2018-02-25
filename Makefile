PY_DIRS := puro tests

all:
	tox

clean:
	rm -rvf .tox

check-format:
	autoflake --recursive --remove-unused-variables $(PY_DIRS)
	autopep8 --diff --recursive --experimental --aggressive --max-line-length=120 $(PY_DIRS)
	isort --diff --recursive $(PY_DIRS)

