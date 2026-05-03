# app/cli/main.py
import click
from rich.console import Console
from rich.table import Table
from rich.progress_bar import ProgressBar
from datetime import datetime, date
from uuid import UUID

from ..config import DATABASE_URL
from ..repositories.database import SessionLocal, engine, Base
from ..repositories.sqlalchemy_repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyProfileRepository,
    SQLAlchemyMealEntryRepository
)
from ..services.auth_service import AuthService
from ..services.user_service import UserService
from ..services.calorie_service import CalorieService
from ..services.progress_service import ProgressService
from ..utils.session import get_current_user_id, save_current_user_id, clear_session
from ..utils.exceptions import CalorieTrackerError
from ..utils.logging import setup_logging

console = Console()
setup_logging()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Объявим контекстный объект для зависимостей (можно через click.pass_context)
...  