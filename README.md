# My_blog project

note:

to run manage.py in production, run the command as follow:

```bash
export DJANGO_SETTINGS_MODULE=My_blog.settings.production; python manage.py runserver ./
```

## Pre Commit

pre-commit is used to maintain code quality.

for first time setup:

```bash
pip install -r requirements/local.txt
pre-commit install
pre-commit run --all-files
```

## First Time install locally

```bash
virtualenv -p python3  env
source env/bin/activate
pip install -r requirements/local.txt
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser --email admin@example.com --username admin
git init
pre-commit install
pre-commit run --all-files
git commit -m "first commit"
```
