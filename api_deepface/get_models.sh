#!/bin/sh

model_path=/root/.deepface/weights
source_path=./deepface_models
deepface_path="https://github.com/serengil/deepface_models/releases/download/v1.0"

mkdir -p -m 755 "$model_path"
if test -d "$source_path"; then
    mv "$source_path"/* "$model_path"
else
    wget "$deepface_path"/age_model_weights.h5 -O "$model_path"/age_model_weights.h5 && \
    wget "$deepface_path"/arcface_weights.h5 -O "$model_path"/arcface_weights.h5 && \
    wget "$deepface_path"/facenet_weights.h5 -O "$model_path"/facenet_weights.h5 && \
    wget "$deepface_path"/facenet512_weights.h5 -O "$model_path"/facenet512_weights.h5 && \
    wget "$deepface_path"/gender_model_weights.h5 -O "$model_path"/gender_model_weights.h5 && \
    wget "$deepface_path"/facial_expression_model_weights.h5 -O "$model_path"/facial_expression_model_weights.h5 && \
    wget "$deepface_path"/vgg_face_weights.h5 -O "$model_path"/vgg_face_weights.h5 && \
    wget "$deepface_path"/retinaface.h5 -O "$model_path"/retinaface.h5 && \
    wget "$deepface_path"/openface_weights.h5 -O "$model_path"/openface_weights.h5 && \
    wget "$deepface_path"/deepid_keras_weights.h5 -O "$model_path"/deepid_keras_weights.h5 && \
    curl -L "https://drive.google.com/u/0/uc?id=1qcr9DbgsX3ryrz2uU8w4Xm3cOrRywXqb&export=download" \
      -o "$model_path"/google_drive_model.h5
fi
