install:
	echo "Installing dependencies"
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt
	echo "Installing pre-commit hooks"
	pre-commit install

makemigrations:
	python3 manage.py makemigrations --settings=config.settings.dev

migrate:
	python3 manage.py migrate --settings=config.settings.dev

createsuperuser:
	python3 manage.py createsuperuser --settings=config.settings.dev

run:
	python3 manage.py runserver --settings=config.settings.dev

shell:
	python3 manage.py shell --settings=config.settings.dev

test:
	pytest
