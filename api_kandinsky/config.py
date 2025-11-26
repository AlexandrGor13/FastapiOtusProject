import logging
from diffusers import KandinskyCombinedPipeline, KandinskyPriorPipeline, KandinskyImg2ImgPipeline

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname).1s %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S'
)

log = logging.getLogger(__name__)

# # Загрузка модели
model_id = "kandinsky-community/kandinsky-2-1"
pipe_text = KandinskyCombinedPipeline.from_pretrained(model_id)

# create prior
pipe_prior = KandinskyPriorPipeline.from_pretrained(f"{model_id}-prior")

prompt_g = "3D cartoon version... soft lighting and clean edges"

image_emb, zero_image_emb = pipe_prior(prompt_g, return_dict=False)

# create img2img pipeline
pipe = KandinskyImg2ImgPipeline.from_pretrained(model_id)
