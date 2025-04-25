FROM python:3-slim AS build-env

WORKDIR /app
COPY requirements.txt config.toml *.py /app

RUN pip install -Ur requirements.txt
CMD ["python3", "power-reporter.py"]
