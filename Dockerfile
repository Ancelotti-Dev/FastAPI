FROM python:3.13.5-slim-bullseye

RUN python --version

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root

RUN pip install --upgrade pip && pip install poetry

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]