#!/usr/bin/make --file

SHELL := bash
.SHELLFLAGS := -euo pipefail -c

.ONESHELL:

UID := $(shell id -u)
GID := $(shell id -g)

DOCKER_REPOSITORY := jump/data-platform


##@ General
.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Build the test
.PHONY: build
build: ## construit l'image Docker qui embarque la CLI, le projet DBT, etc.
	mkdir -p "./data"
	docker build \
		--build-arg "UID=$(UID)" \
		--build-arg "GID=$(GID)" \
		--file "./docker/Dockerfile" \
		--tag "$(DOCKER_REPOSITORY)" \
			"."


##@ Data
.PHONY: extract
extract: ## lance l'extract des données de l'application et du CRM
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)" \
			extract


.PHONY: transform
transform: ## transforme les données et alimente les schémas "staging", "intermediate" et "bronze"
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		--volume "$(PWD)/dbt:/usr/local/lib/data-platform/dbt" \
		"$(DOCKER_REPOSITORY)" \
			transform


.PHONY: load
load: # lance l'inégration des extractions dans le schéma "source" du Lakehouse
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)" \
			load


##@ Internal
.PHONY: all
all:
	mkdir -p "./data"
	docker run \
		--rm \
		--user "$(UID):$(GID)" \
		--volume "$(PWD)/data:/var/local/lib/data-platform" \
		"$(DOCKER_REPOSITORY)"


.PHONY: debug
debug: build ## Lance une console interactive dans le docker de test
	mkdir -p "./data"
	docker run \
		--interactive \
		--tty \
		--rm \
		--entrypoint "/bin/bash" \
		"$(DOCKER_REPOSITORY)"


.PHONY: clean
clean: ## Clean the project
	rm -rf "./data"