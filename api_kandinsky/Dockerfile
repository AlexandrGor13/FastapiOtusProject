FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TRANSFORMERS_CACHE="/var/model"

WORKDIR /var/app

RUN pip3 install --upgrade pip
RUN pip3 install transformers[torch] huggingface-hub
RUN mkdir models && cd models
RUN huggingface-cli download "kandinsky-community/kandinsky-2-1"

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt


COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]