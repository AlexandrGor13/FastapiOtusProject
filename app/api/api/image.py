from typing import List
from fastapi import APIRouter, File, UploadFile, status
import io
from PIL import Image
import numpy as np
from deepface import DeepFace

router = APIRouter(tags=["DeepFace"], prefix="/image")


@router.post(
    "/recognize-face/",
    status_code = status.HTTP_200_OK,
    summary = "Recognize Face",
    responses = {
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
    # Загрузка файла
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))

    # Преобразование изображения в массив NumPy
    image_array = np.array(img)

    try:
        result = DeepFace.analyze(image_array, actions=('age', 'gender', 'emotion'))
        if len(result) != 1:
            raise ValueError('На изображении более одного лица')
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
        return {"error": str(e)}


@router.post(
    "/compare-faces/",
    status_code=status.HTTP_200_OK,
    summary="Compare Faces",
    responses={
        status.HTTP_200_OK: {
            "description": "Compare Faces",
            "content": {
                "application/json": {
                    "example": {
                        "verified": 'true',
                        "distance": 0.516673,
                        "model": "VGG-Face"
                    }
                }
            }
        }
    }
)
async def compare_faces(files: List[UploadFile]):
    """
    Сравнивает два загруженных изображения на предмет схожести лиц.
    """
    if len(files) != 2:
        return {"error": "Необходимо загрузить ровно два изображения"}

    images = []
    for file in files:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        image_array = np.array(img)
        images.append(image_array)

    try:
        result = DeepFace.verify(images[0], images[1])
        print(result)
        return {
            "verified": result.get("verified"),
            "distance": result.get("distance"),
            'model': result.get("model"),
        }
    except Exception as e:
        return {"error": str(e)}
