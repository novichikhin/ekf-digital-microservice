FROM python:3.10

WORKDIR .

COPY poetry.lock pyproject.toml ./

RUN python3.10 -m pip install poetry
RUN poetry install --no-dev

COPY . .

CMD poetry run python -m ekf_digital_microservice.queue.rabbitmq.digest