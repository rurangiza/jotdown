# name
ENTRYPOINT := main

# directories
CURRENT_DIR := $(shell pwd)
SRC_DIR := jotdown


# variables
INTERPRETER := python3

# commands
export PYTHONPATH := $(CURRENT_DIR)

# colors
COLOUR_GREEN=\033[0;32m
COLOUR_RED=\033[0;31m
COLOUR_BLUE=\033[0;34m
COLOUR_END=\033[0m


# rules
all: run

run:
	@$(INTERPRETER) $(SRC_DIR)/$(ENTRYPOINT).py

test:
	@pytest

hello:
	@echo "$(COLOUR_GREEN)Starting the program..$(COLOUR_END)"

build:
	@pip install -r requirements.txt
	@echo "$(COLOUR_GREEN)Finished installing dependencies.$(COLOUR_END)"

req:
	@pip freeze > requirements.txt
# pip show <module_name>

clean:
	@rm -rf db
	@echo "$(COLOUR_BLUE)Deleted the database$(COLOUR_END)"

.PHONY: all run test install req
