SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make deploy -- deploy to <hosting>"
	@echo "    make static -- build static files to s3"

deploy:
	@echo "You should set this up."

static:
	STATICFILES_STORAGE='storages.backends.s3boto.S3BotoStorage' python manage.py collectstatic -i *.sass --noinput
