FROM python:3.6-jessie

LABEL author="Rodrigo L. Gil"

COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y cron && pip install --upgrade pip && pip install -r /code/requirements.txt

COPY app/ /code/app/
COPY conf/ /code/conf/
COPY domain/ /code/domain/
COPY request/ /code/request/
COPY util/ /code/util/

COPY definitions.py /code/definitions.py

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV PYTHONPATH=/code/
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /code/