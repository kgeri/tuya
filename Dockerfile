FROM python:3-slim AS build-env

WORKDIR /app
COPY requirements.txt /app
RUN pip install -Ur requirements.txt
COPY config.toml *.py /app

CMD ["python3", "power-reporter.py"]
