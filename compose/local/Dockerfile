FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /

COPY ./requirements/base.txt /requirements/base.txt
COPY ./requirements/local.txt /requirements/local.txt
RUN pip install --cache-dir=/root/.pip -r ./requirements/local.txt

COPY ./compose/production/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/start.sh /
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh
WORKDIR /code
COPY . /code/

ENTRYPOINT ["/entrypoint"]
