FROM python:3.9-buster

WORKDIR /app

COPY src .
COPY poetry.lock .
COPY pyproject.toml .

RUN python3 -m pip install poetry
RUN python3 -m pip install pycryptodome
RUN python3 -m pip uninstall apibara
RUN python3 -m pip install apibara
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT [ "indexer" ]
CMD ["indexer", "start", "--restart"]
CMD ["indexer", "graphql"]