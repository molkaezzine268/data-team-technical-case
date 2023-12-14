#!/usr/bin/make --file

SHELL := bash
.SHELLFLAGS := -euo pipefail -c

.ONESHELL:

UID := $(shell id -u)
GID := $(shell id -g)

DOCKER_REPOSITORY := jump/data-platform


.PHONY: build
build:
	mkdir -p "./data"
	docker build \
		--build-arg "UID=$(UID)" \
		--build-arg "GID=$(GID)" \
		--progress="plain" \
		--file "./docker/Dockerfile" \
		--tag "$(DOCKER_REPOSITORY)" \
			"."


.PHONY: extract
extract:
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)" \
			extract


.PHONY: transform
transform:
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		--volume "$(PWD)/dbt:/usr/local/lib/data-platform/dbt" \
		"$(DOCKER_REPOSITORY)" \
			transform


.PHONY: load
load:
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)" \
			load


.PHONY: all
all:
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)"


.PHONY: debug
debug: build
	docker run \
		--interactive \
		--tty \
		--rm \
		--entrypoint "/bin/bash" \
		"$(DOCKER_REPOSITORY)"


.PHONY: clean
clean:
	rm -rf "./data"