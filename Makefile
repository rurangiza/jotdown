
INTERPRETER := python3
CURRENT_DIR := $(shell pwd)

export PYTHONPATH := $(CURRENT_DIR)

all: build

init: .init_done

.init_done:
	touch .init_done

build: init
	@$(INTERPRETER) letschat/app.py

test: init
	@$(INTERPRETER) tests/test_stream.py

dev:


clean:
	rm -rf .init_done