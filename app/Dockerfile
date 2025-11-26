FROM python:3.12
WORKDIR /var/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip "uv==0.6.14"

COPY pyproject.toml uv.lock ./

ENV PATH="/var/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app ./

RUN chmod +x ./entrypoint.sh

ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=2

ENTRYPOINT ["./entrypoint.sh"]