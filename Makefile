export PYTHON_EXEC = python3.10
export NODE_VERSION = 16.14.2
export NPM_VERSION = 8.5.0
SHELL := /bin/bash
VENV="${CURDIR}/.venv"

.PHONY: venv

venv:
	$(PYTHON_EXEC) -m venv .venv
	source ${VENV}/bin/activate && pip install -U pip wheel nodeenv
	source ${VENV}/bin/activate && nodeenv -p -n $(NODE_VERSION)
	source ${VENV}/bin/activate && npm install -g npm@$(NPM_VERSION)
	source ${VENV}/bin/activate && npm install -g yarn

