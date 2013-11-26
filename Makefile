PYFILES := $(shell git ls-files '*.py')

.PHONY: lint
lint: .venv .venv3
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pylint $(PYFILES)
	.venv3/bin/pip install -r requirements.txt
	.venv3/bin/pylint $(PYFILES)
	@echo '--- DING! ---'

.venv:
	virtualenv --prompt='[python2] ' -p python2.7 $@

.venv3:
	virtualenv --prompt='[python3] ' -p python3.3 $@
