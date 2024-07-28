FROM python:3.12-slim

RUN pip install --upgrade pip --no-cache-dir

WORKDIR /app

RUN pip install gunicorn==20.1.0
RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root --no-cache

COPY . .

CMD ["gunicorn", "weather_forecast.wsgi", "--bind", "0.0.0.0:8000"]