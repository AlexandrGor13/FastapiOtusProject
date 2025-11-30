from typing import Annotated
from io import BytesIO
import requests
from fastapi import APIRouter, File, UploadFile, status, Body, Form, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from dependencies.dependencies import get_current_user
from core.config import settings

router = APIRouter(prefix="/image")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post(
    "/recognize-face",
    status_code=status.HTTP_200_OK,
    summary="Recognize Face",
    tags=["DeepFace"],
    dependencies=[Depends(get_current_user)],
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
    if not allowed_file(file.filename):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"Неверное расширение файла '{file.filename}'. "
                         f"Допустимые расширения {list(ALLOWED_EXTENSIONS)}"},
        )
    try:
        image_bytes = await file.read()

        response = requests.post(
            f'http://{settings.api.deepface_host}:{settings.api.deepface_port}/recognize-face',
            files={'file': (file.filename, image_bytes)}
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Ошибка обработки изображения внешним сервисом ({response.status_code})"},
            )

        return response.json()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@router.post(
    "/compare-faces",
    status_code=status.HTTP_200_OK,
    summary="Compare Faces",
    tags=["DeepFace"],
    dependencies=[Depends(get_current_user)],
    responses={
        status.HTTP_200_OK: {
            "description": "Compare Faces",
            "content": {
                "application/json": {
                    "example": {
                        "verified": True,
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

    if not allowed_file(file1.filename) and not allowed_file(file2.filename):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"Неверное расширение файлов '{file1.filename}' или '{file2.filename}'. "
                         f"Допустимые расширения {list(ALLOWED_EXTENSIONS)}"},
        )
    try:
        image_bytes1 = await file1.read()
        image_bytes2 = await file2.read()
        response = requests.post(
            f'http://{settings.api.deepface_host}:{settings.api.deepface_port}/compare-faces',
            files={'file1': (file1.filename, image_bytes1),
                   'file2': (file2.filename, image_bytes2)
                   },
            params={'model_name': model_name}
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Ошибка обработки изображения внешним сервисом ({response.status_code})"},
            )

        return response.json()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@router.post(
    "/count-people",
    status_code=status.HTTP_200_OK,
    summary="Count people",
    tags=["DeepFace"],
    dependencies=[Depends(get_current_user)],
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

    if not allowed_file(file.filename):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"Неверное расширение файла '{file.filename}'. "
                         f"Допустимые расширения {list(ALLOWED_EXTENSIONS)}"},
        )
    try:
        image_bytes = await file.read()
        response = requests.post(
            f'http://{settings.api.deepface_host}:{settings.api.deepface_port}/count-people',
            files={'file': (file.filename, image_bytes)}
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Ошибка обработки изображения внешним сервисом ({response.status_code})"},
            )

        return response.json()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@router.post(
    "/generate_image",
    status_code=status.HTTP_200_OK,
    summary="Generate image",
    tags=["Kandinsky"],
    dependencies=[Depends(get_current_user)],
)
async def generate_image(prompt: str = Form(..., max_length=60)):
    """
    Генерирует изображение по описанию.
    """

    try:
        response = requests.post(
            f'http://{settings.api.kandinsky_host}:{settings.api.kandinsky_port}/generate_image',
            data={"prompt": prompt},
            stream=True
        )
        response.raise_for_status()
        if response.status_code == 200:
            buffer = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    buffer.write(chunk)
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="image/png")
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Ошибка обработки изображения внешним сервисом ({response.status_code})"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@router.post(
    "/generate_avatar",
    status_code=status.HTTP_200_OK,
    summary="Generate avatar",
    tags=["Kandinsky"],
    dependencies=[Depends(get_current_user)],
)
async def generate_avatar(file: UploadFile = File(...)):
    """
    Генерирует уникальный аватар по фотографии пользователя и возвращает результат в виде потока байтов.
    """

    if not allowed_file(file.filename):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"Неверное расширение файла '{file.filename}'. "
                         f"Допустимые расширения {list(ALLOWED_EXTENSIONS)}"},
        )

    prompt = "стиль анимации, уникальный, добрый"
    try:
        image_bytes = await file.read()
        response = requests.post(
            f'http://{settings.api.kandinsky_host}:{settings.api.kandinsky_port}/generate_avatar',
            files={'file': (file.filename, image_bytes)},
            data={"prompt": prompt},
            stream=True
        )
        response.raise_for_status()
        if response.status_code == 200:
            buffer = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    buffer.write(chunk)
            buffer.seek(0)
            return StreamingResponse(buffer, media_type="image/png")
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Ошибка обработки изображения внешним сервисом ({response.status_code})"},
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )
