FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/app
COPY ./requirements.txt ./

RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

WORKDIR /var/models
RUN huggingface-cli download "kandinsky-community/kandinsky-2-1" --local-dir .
ENV HF_HOME="/var/models"

WORKDIR /var/app
COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
