SHELL := /bin/bash

env-setup:
	rm -rf venv
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt


run-local:
	pip install -r requirements.txt;
	python manage.py makemigrations; \
	python manage.py migrate; \
	python manage.py runserver 8000


test:
    python manage.py test