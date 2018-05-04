FROM python:3.6-jessie

LABEL author="Rodrigo L. Gil"

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y cron && pip install -r /code/requirements.txt

COPY request_api/ /code/request_api/
COPY util/ /code/util
COPY definitions.py /code/definitions.py
COPY flask_app.py /code/flask_app.py

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /code/