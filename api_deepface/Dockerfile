FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /var/app

COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 wget curl

RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
    
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./ ./

RUN chmod +x ./get_models.sh && ./get_models.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
