.PHONY : install test build release

install:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt

test:
	ruff . && \
	python3 -m unittest

build:
	python3 -m build

release:
	.github/release.sh ${bump}