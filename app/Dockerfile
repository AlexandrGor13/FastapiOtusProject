FROM python:3.12
WORKDIR /var/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip "uv==0.6.14"

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

ENV PATH="/var/app/.venv/bin:$PATH"

COPY ./app ./


RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]