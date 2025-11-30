from typing import Annotated
from io import BytesIO
from PIL import Image
import numpy as np
import requests

from fastapi import APIRouter, File, UploadFile, status, Body, Depends
from fastapi.responses import JSONResponse

from deepface import DeepFace
from deepface.modules.detection import extract_faces

from config import log

router = APIRouter()


@router.post(
    "/recognize-face",
    status_code=status.HTTP_200_OK,
    summary="Recognize Face",
    tags=["DeepFace"],
    responses={
        status.HTTP_200_OK: {
            "description": "Recognize Face",
            "content": {
                "application/json": {
                    "example": {
                        "result": "Возраст: 35, Пол: мужчина, Эмоция: нейтральная",
                        "age": 35,
                        "gender": "Man",
                        "emotion": "neutral"
                    }
                }
            }
        }
    }
)
async def recognize_face(file: UploadFile = File(...)):
    """
    Определяет возраст, пол и эмоцию лица на изображении.
    """

    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        image_array = np.array(img)

        faces = extract_faces(image_array, detector_backend='yolov8n')
        if len(faces) != 1:
            raise ValueError('На изображении должно быть одно лицо')

        result = DeepFace.analyze(image_array, actions=('age', 'gender', 'emotion'), detector_backend='yolov8n')
        img_age = result[0].get('age')
        img_gender = 'мужчина' if result[0].get('dominant_gender') == 'Man' else 'женщина'
        img_emotion = result[0].get('dominant_emotion')
        match img_emotion:
            case 'angry':
                img_emotion = 'сердитый'
            case 'disgust':
                img_emotion = 'отвращение'
            case 'fear':
                img_emotion = 'страх'
            case 'happy':
                img_emotion = 'счастливый'
            case 'sad':
                img_emotion = 'грустный'
            case 'surprise':
                img_emotion = 'удивление'
            case 'neutral':
                img_emotion = 'нейтральная'
        return {
            "result": f"Возраст: {img_age}, Пол: {img_gender}, Эмоция: {img_emotion}",
            "age": img_age,
            "gender": result[0].get('dominant_gender'),
            "emotion": result[0].get('dominant_emotion'),
        }
    except Exception as e:
        log.error("An exception occurred: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)},
        )


@router.post(
    "/compare-faces",
    status_code=status.HTTP_200_OK,
    summary="Compare Faces",
    tags=["DeepFace"],
    responses={
        status.HTTP_200_OK: {
            "description": "Compare Faces",
            "content": {
                "application/json": {
                    "example": {
                        "verified": 'true',
                        "distance": 0.516673,
                    }
                }
            }
        }
    }
)
async def compare_faces(
        file1: UploadFile = File(...),
        file2: UploadFile = File(...),
        model_name: Annotated[str,
        Body(...,
             description="Model for face recognition. Options: VGG-Face, Facenet, Facenet512, DeepFace, ArcFace"
             )] = "VGG-Face"
):
    """
    Сравнивает два загруженных изображения на предмет схожести лиц.
    """

    try:
        images = []
        for file in file1, file2:
            contents = await file.read()
            img = Image.open(BytesIO(contents))
            image_array = np.array(img)
            faces = extract_faces(image_array, detector_backend='yolov8n')
            if len(faces) != 1:
                raise ValueError('На изображении должно быть одно лицо')
            images.append(image_array)
        result = DeepFace.verify(images[0], images[1], model_name=model_name)
        return {
            "verified": result.get("verified"),
            "distance": result.get("distance"),
        }
    except Exception as e:
        log.error("An exception occurred: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)},
        )


@router.post(
    "/count-people",
    status_code=status.HTTP_200_OK,
    summary="Count people",
    tags=["DeepFace"],
    responses={
        status.HTTP_200_OK: {
            "description": "Count people",
            "content": {
                "application/json": {
                    "example": {
                        "count people": 2
                    }
                }
            }
        }
    }
)
async def count_people(file: UploadFile = File(...)):
    """
    Сравнивает два загруженных изображения на предмет схожести лиц.
    """

    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        image_array = np.array(img)
        result = extract_faces(image_array, detector_backend='yolov8n')
        return {
            "count people": len(result),
        }
    except Exception as e:
        log.error("An exception occurred: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)},
        )
