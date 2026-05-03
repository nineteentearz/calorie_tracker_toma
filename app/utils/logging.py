# app/utils/logging.py
import logging
from ..config import LOG_FILE

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()  # можно убрать, если не нужен вывод в консоль
        ]
    )
    # Подавляем логи SQLAlchemy, кроме ошибок
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)