PYFILES := $(shell git ls-files '*.py')

.PHONY: all
all: lint test

.PHONY: lint
lint: .py2lint .py3lint
	@echo '--- DING! ---'

.PHONY: test
test: .py2test .py3test
	@echo '--- YAY! ---'

.PHONY: .py2test
.py2test: .py2reqs
	source .venv/bin/activate && ./runtests

.PHONY: .py3test
.py3test: .py3reqs
	source .venv3/bin/activate && ./runtests

.PHONY: .py2lint
.py2lint: .py2reqs
	.venv/bin/pylint -f colorized $(PYFILES)

.PHONY: .py3lint
.py3lint: .py3reqs
	.venv3/bin/pylint -f colorized $(PYFILES)

.PHONY: reqs
reqs: .py2reqs .py3reqs

.PHONY: .py2reqs
.py2reqs: .venv
	.venv/bin/pip install -r requirements.txt

.PHONY: .py3reqs
.py3reqs: .venv3
	.venv3/bin/pip install -r requirements.txt

.venv:
	virtualenv --prompt='[python2] ' -p python2.7 $@

.venv3:
	virtualenv --prompt='[python3] ' -p python3.3 $@
