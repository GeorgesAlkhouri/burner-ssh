.PHONY: dev build

dev:
	docker run --rm -it -v $(PWD):/shared onionssh bash


build:
	docker build -t onionssh -f ./dev/Dockerfile .


