import logging

logging.basicConfig(
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ],
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s "
)

logger = logging.getLogger(__name__)

logging.getLogger("watchfiles").setLevel(logging.WARNING)