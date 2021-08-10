.PHONY: dev build

dev:
	docker run --rm -it -v $(PWD):/shared onionssh bash

build:
	docker build -t onionssh -f ./dev/Dockerfile .

compile:
	pip-compile --output-file requirements/prod.txt setup.cfg
	pip-compile --output-file requirements/dev.txt requirements/dev.in

sync:
	pip-sync requirements/*.txt

re-compile: compile sync

