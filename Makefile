
# name
ENTRYPOINT := main

# directories
CURRENT_DIR := $(shell pwd)
SRC_DIR := letschat


# variables
INTERPRETER := python3

# commands
export PYTHONPATH := $(CURRENT_DIR)


# rules
all: run

run:
	@$(INTERPRETER) $(SRC_DIR)/$(ENTRYPOINT).py

test:
	@pytest

install:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt
	# pip show <module_name>

.PHONY: all run test install req
