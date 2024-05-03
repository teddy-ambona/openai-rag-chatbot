.PHONY: app-build app-run db-up db-down db-populate clean

PYTHON_VERSION = 3.11
DRUN = docker run --rm
DBASH = $(DRUN) -u root -v ${PWD}:/foo -w="/foo" python:$(PYTHON_VERSION) bash -c
IMAGE_NAME = openai-rag-chatbot-app
IMAGE_VERSION = 0.0.0

# ============================================================
# App commands
# ============================================================

## Buid Docker image of Langserve app
app-build:
	docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .

## Run Docker image
app-run:
	docker compose up app

## Return API version (useful for tagging Docker image in CI)
app-get-version:
	echo ${IMAGE_NAME}:${IMAGE_VERSION}

# ============================================================
# DB commands
# ============================================================

## Start DB
db-up:
	docker-compose up -d milvus-standalone

## Stop DB
db-down:
	docker compose down

## Populate DB with the LASIK eye surgery complications dataset
db-populate:
	docker compose run db-populate

## Delete all compiled Python files and Milvus volumes
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "_pycache_" -delete
	find . -type d -name "*.egg-info" -exec rm -r "{}" +
	find . -type d -name ".pytest_cache" -exec rm -r "{}" +
	rm -rf  volumes

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by ---
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
