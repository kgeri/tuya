FROM python:3-slim-bullseye

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY config.toml *.py /app

CMD ["python3", "power-reporter.py"]
