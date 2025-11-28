import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelprefix)s | %(asctime)s | %(module)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)

