FROM python:3.10-slim as builder

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .

# Compile Cython extensions
RUN python setup.py build_ext --inplace

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

CMD ["uvicorn", "api.fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
