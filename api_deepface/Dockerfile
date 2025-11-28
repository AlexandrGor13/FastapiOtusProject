FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /var/app

COPY ./requirements.txt ./

ADD https://github.com/serengil/deepface_models/releases/download/v1.0/age_model_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/arcface_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/facenet512_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/gender_model_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/vgg_face_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/retinaface.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/openface_weights.h5 /root/.deepface/weights/
ADD https://github.com/serengil/deepface_models/releases/download/v1.0/deepid_keras_weights.h5 /root/.deepface/weights/
ADD https://drive.google.com/uc?id=1qcr9DbgsX3ryrz2uU8w4Xm3cOrRywXqb /root/.deepface/weights/

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]