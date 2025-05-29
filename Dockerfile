FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./scripts/entrypoint.sh ./scripts/wait-for-it.sh

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["python", "-m", "src.main"]
