.ONESHELL:

.PHONY: bin venv

BIN=venv/bin
PIP=venv/bin/pip
PY_FILES := $(wildcard byhand/*.py setup.py)

bin: dist/byhand

dist/byhand: $(PY_FILES) venv/touchfile
	mkdir -p dist
	$(BIN)/shiv -c byhand -o dist/byhand .

venv: venv/touchfile

venv/touchfile:
	test -d venv || python3 -m venv venv
	$(PIP) install shiv
	touch venv/touchfile

clean:
	rm -rf build dist byhand.egg-info venv
