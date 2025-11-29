FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/app

RUN pip install --upgrade pip "uv==0.6.14"

COPY pyproject.toml uv.lock ./

ENV PATH="/var/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-dev

COPY ./app ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]