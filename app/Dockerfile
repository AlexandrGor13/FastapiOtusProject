FROM python:3.12
WORKDIR /var/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip "uv==0.6.14"

COPY pyproject.toml uv.lock ./

ENV PATH="/var/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-dev

COPY ./app ./

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]