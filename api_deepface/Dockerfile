FROM python:3.12

ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=2

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]