import logging


logging.basicConfig(
    format="%(asctime)s | %(level)s | %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ],

)

logger = logging.getLogger(__name__)