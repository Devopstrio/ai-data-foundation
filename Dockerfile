FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install .

COPY src/ src/

CMD ["python", "src/aidatafoundation/main.py"]
