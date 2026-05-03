import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "calories.db"
SESSION_FILE = BASE_DIR / ".session"
LOG_FILE = BASE_DIR / "calorie_tracker.log"

DATABASE_URL = f"sqlite:///{DB_PATH}"

DB_RETRY_MAX = 3
DB_RETRY_WAIT = 0.5

BCRYPT_ROUNDS = 12