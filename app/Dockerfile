FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/app_api

RUN pip install --upgrade pip "uv==0.6.14"

COPY pyproject.toml uv.lock ./

ENV PATH="/var/app_api/.venv/bin:$PATH"

RUN uv sync --frozen --no-dev

COPY ./app ./app

RUN mv ./app/alembic.ini ./
RUN mv ./app/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]