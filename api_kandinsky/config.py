import logging
from diffusers import (
    KandinskyCombinedPipeline,
    KandinskyPriorPipeline,
    KandinskyImg2ImgPipeline,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelprefix)s | %(asctime)s | %(module)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)
model_id = "kandinsky-community/kandinsky-2-1"

# Загрузка модели для генерации изображения по описанию
pipe_text = KandinskyCombinedPipeline.from_pretrained(model_id)

# Загрузка модели для генерации предварительных изображений
pipe_prior = KandinskyPriorPipeline.from_pretrained(f"{model_id}-prior")

# Загрузка модели для генерации изображений
pipe = KandinskyImg2ImgPipeline.from_pretrained(model_id)
