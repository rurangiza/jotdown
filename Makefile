NAME := app
INTERPRETER := python

all: run

run:
	$(INTERPRETER) $(NAME).py

init:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt
	# pip show <module_name>