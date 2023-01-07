SHELL = /bin/bash
CURRENT_DIR = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

default:
	@echo "--------- Quant Commands ---------"
	@echo "make create-venv"						# Creates the virtual environment
	@echo "make install-venv"						# Installs virtual environment
	@echo "make start-venv"							# Starts the virtual environment
	@echo "make setup"									# Installs all python dependencies

install-venv:
	pip install virtualenv

create-venv:
	virtualenv venv

test:
	pytest

alias:
	alias python=python3
	alias pip=pip3
	
setup:
	pip install -r requirements.txt
	@echo $(CURRENT_DIR)
