#!/usr/bin/make --file

SHELL := bash
.SHELLFLAGS := -euo pipefail -c

.ONESHELL:

UID := $(shell id -u)
GID := $(shell id -g)

DOCKER_REPOSITORY := jump/data-platform


.PHONY: build
build:
	docker build \
		--build-arg "UID=$(UID)" \
		--build-arg "GID=$(GID)" \
		--progress="plain" \
		--file "./docker/Dockerfile" \
		--tag "$(DOCKER_REPOSITORY)" \
			"."


.PHONY: extract
extract: build
	docker run --rm "$(DOCKER_REPOSITORY)" extract

.PHONY: transform
transform: build
	docker run --rm "$(DOCKER_REPOSITORY)" transform

.PHONY: load
load: build
	docker run --rm "$(DOCKER_REPOSITORY)" load

.PHONY: all
all: build
	docker run --rm "$(DOCKER_REPOSITORY)"

.PHONY: debug
debug: build
	docker run \
		--interactive \
		--tty \
		--rm \
		--entrypoint "/bin/bash" \
		"$(DOCKER_REPOSITORY)"