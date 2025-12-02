from io import BytesIO
from PIL import Image

from fastapi import APIRouter, File, UploadFile, status, Form
from fastapi.responses import StreamingResponse, JSONResponse

from config import pipe, pipe_prior, pipe_text, log

router = APIRouter()


@router.post(
    "/generate_image",
    status_code=status.HTTP_200_OK,
    summary="Generate image",
    tags=["Kandinsky"],
)
async def generate_image(prompt: str = Form(...)):
    """
    Генерирует изображение по описанию.
    """

    try:
        image = pipe_text(
            prompt,
            num_inference_steps=50,
        ).images[0]

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


@router.post(
    "/generate_avatar",
    status_code=status.HTTP_200_OK,
    summary="Generate avatar",
    tags=["Kandinsky"],
)
async def generate_avatar(file: UploadFile = File(...), prompt: str = Form(...)):
    """
    Генерирует уникальный аватар по фотографии пользователя и возвращает результат в виде потока байтов.
    """

    try:
        img_bytes = await file.read()
        input_image = Image.open(BytesIO(img_bytes))
        input_image.thumbnail((768, 768))

        image_emb, zero_image_emb = pipe_prior(prompt, return_dict=False)

        image = pipe(
            prompt,
            image=input_image,
            image_embeds=image_emb,
            negative_image_embeds=zero_image_emb,
            height=768,
            width=768,
            num_inference_steps=120,
            strength=0.15,
        ).images[0]

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
