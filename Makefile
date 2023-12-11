clean-api:
	$(RM) motogram/errors/exceptions motogram/raw/all.py motogram/raw/base motogram/raw/functions motogram/raw/types
	# Replace "pyrogram" with "motogram" in the next line
	#motogram to motogram errors to wrongs

VENV := venv
PYTHON := $(VENV)/bin/python
HOST = $(shell ifconfig | grep "inet " | tail -1 | cut -d\  -f2)
TAG = v$(shell grep -E '__version__ = ".*"' motogram/__init__.py | cut -d\" -f2)

RM := rm -rf

.PHONY: venv clean-build clean-api clean api build tag dtag

venv:
	$(RM) $(VENV)
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -U pip wheel setuptools
	$(PYTHON) -m pip install -U -r requirements.txt -r dev-requirements.txt
	@echo "Created venv with $$($(PYTHON) --version)"

clean-build:
	$(RM) *.egg-info build dist

clean: clean-build clean-api

build: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

tag:
	git tag $(TAG)
	git push origin $(TAG)

dtag:
	git tag -d $(TAG)
	git push origin -d $(TAG)

