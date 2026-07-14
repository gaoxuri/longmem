FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 8123

# Auto-create the vector extension + table on boot, then serve.
CMD ["sh", "-c", "python -c 'from longmem import init_db; init_db()' && python -m longmem.api"]
