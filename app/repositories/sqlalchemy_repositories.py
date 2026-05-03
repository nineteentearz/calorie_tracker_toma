# app/repositories/sqlalchemy_repositories.py
import logging
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed
from ..domain.models import User, Profile, MealEntry
from ..domain.repositories import (
    UserRepository, ProfileRepository, MealEntryRepository
)
from ..config import DB_RETRY_MAX, DB_RETRY_WAIT
from .orm_models import UserModel, ProfileModel, MealEntryModel
from ..utils.exceptions import RepositoryError

logger = logging.getLogger(__name__)

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def add(self, user: User) -> None:
        try:
            user_model = UserModel(
                id=user.id,
                email=user.email,
                hashed_password=user.hashed_password,
                created_at=user.created_at,
                is_active=user.is_active
            )
            self.session.add(user_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add user: {e}")
            raise RepositoryError(f"Database error: {e}")

    @retry(...)
    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
            if not user_model:
                return None
            return User(
                id=user_model.id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                created_at=user_model.created_at,
                is_active=user_model.is_active
            )
        except Exception as e:
            raise RepositoryError(f"Database error: {e}")

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        ... # аналогично

# Аналогично ProfileRepository, MealEntryRepository (я напишу полностью в финальном коде)