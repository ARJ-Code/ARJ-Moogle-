cant_lines ?= 1000

.PHONY: dev
dev:
	python src/main.py

.PHONY: build
build:
	python src/build.py $(cant_lines)

