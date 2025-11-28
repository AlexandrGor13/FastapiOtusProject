from io import BytesIO
from PIL import Image

from fastapi import APIRouter, File, UploadFile, status, Form
from fastapi.responses import StreamingResponse, JSONResponse

from config import pipe, log

router = APIRouter()


@router.post(
    "/generate_image",
    status_code=status.HTTP_200_OK,
    summary="Generate image",
    tags=["Kandinsky"],
)
async def generate_image(prompt: str = Form(...)):
    """
    Генерирует изображение по текстовым описаниям
    """

    try:
        image = pipe(prompt).images[0]

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        log.error("An exception occurred: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )


@router.post("/generate_avatar")
async def generate_avatar(file: UploadFile = File(...), prompt: str = Form(...)):
    """
    Генерирует уникальный аватар по фотографии пользователя и возвращает результат в виде потока байтов.
    """

    try:
        img_bytes = await file.read()
        input_image = Image.open(BytesIO(img_bytes))

        image = pipe(prompt, image=input_image).images[0]

        output_buffer = BytesIO()
        image.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        return StreamingResponse(output_buffer, media_type="image/png")

    except Exception as e:
        log.error("An exception occurred: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
