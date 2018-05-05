FROM exchange-rate

LABEL author="Rodrigo L. Gil"

COPY requirements.txt /code/requirements_tests.txt

RUN apt-get update && pip install -r /code/requirements_tests.txt

COPY unit/ /code/tests/unit/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV PYTHONPATH=/code/

ENTRYPOINT ["/entrypoint.sh"]