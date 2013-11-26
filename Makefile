.PHONY: lint
lint: .venv .venv3
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pylint ./loggly_pipe/
	.venv3/bin/pip install -r requirements.txt
	.venv3/bin/pylint ./loggly_pipe/
	@echo '--- DING! ---'

.venv:
	virtualenv --prompt='[python2] ' -p python2.7 $@

.venv3:
	virtualenv --prompt='[python3] ' -p python3.3 $@
