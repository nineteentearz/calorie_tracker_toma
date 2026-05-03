import logging
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed
from ..domain.models import User, Profile, MealEntry
from ..domain.repositories import UserRepository, ProfileRepository, MealEntryRepository
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
                id=str(user.id),
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

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = self.session.query(UserModel).filter(UserModel.email == email).first()
            if not user_model:
                return None
            return User(
                id=UUID(user_model.id),
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                created_at=user_model.created_at,
                is_active=user_model.is_active
            )
        except Exception as e:
            raise RepositoryError(f"Database error: {e}")

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            user_model = self.session.query(UserModel).filter(UserModel.id == str(user_id)).first()
            if not user_model:
                return None
            return User(
                id=UUID(user_model.id),
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                created_at=user_model.created_at,
                is_active=user_model.is_active
            )
        except Exception as e:
            raise RepositoryError(f"Database error: {e}")


class SQLAlchemyProfileRepository(ProfileRepository):
    def __init__(self, session: Session):
        self.session = session

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def save(self, profile: Profile) -> None:
        try:
            profile_model = self.session.query(ProfileModel).filter(ProfileModel.user_id == str(profile.user_id)).first()
            if profile_model:
                profile_model.height_cm = profile.height_cm
                profile_model.weight_kg = profile.weight_kg
                profile_model.age = profile.age
                profile_model.gender = profile.gender
                profile_model.daily_calorie_goal = profile.daily_calorie_goal
                profile_model.updated_at = datetime.utcnow()
            else:
                profile_model = ProfileModel(
                    user_id=str(profile.user_id),
                    height_cm=profile.height_cm,
                    weight_kg=profile.weight_kg,
                    age=profile.age,
                    gender=profile.gender,
                    daily_calorie_goal=profile.daily_calorie_goal,
                    updated_at=datetime.utcnow()
                )
                self.session.add(profile_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to save profile: {e}")
            raise RepositoryError(f"Database error: {e}")

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        try:
            profile_model = self.session.query(ProfileModel).filter(ProfileModel.user_id == str(user_id)).first()
            if not profile_model:
                return None
            return Profile(
                user_id=UUID(profile_model.user_id),
                height_cm=profile_model.height_cm,
                weight_kg=profile_model.weight_kg,
                age=profile_model.age,
                gender=profile_model.gender,
                daily_calorie_goal=profile_model.daily_calorie_goal,
                updated_at=profile_model.updated_at
            )
        except Exception as e:
            raise RepositoryError(f"Database error: {e}")


class SQLAlchemyMealEntryRepository(MealEntryRepository):
    def __init__(self, session: Session):
        self.session = session

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def add(self, entry: MealEntry) -> None:
        try:
            meal_model = MealEntryModel(
                id=str(entry.id),
                user_id=str(entry.user_id),
                product_name=entry.product_name,
                calories=entry.calories,
                date=entry.date,
                created_at=entry.created_at
            )
            self.session.add(meal_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add meal entry: {e}")
            raise RepositoryError(f"Database error: {e}")

    @retry(stop=stop_after_attempt(DB_RETRY_MAX), wait=wait_fixed(DB_RETRY_WAIT))
    def get_by_user_and_date_range(self, user_id: UUID, start_date: date, end_date: date) -> List[MealEntry]:
        try:
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.max.time())
            models = self.session.query(MealEntryModel).filter(
                MealEntryModel.user_id == str(user_id),
                MealEntryModel.date >= start_dt,
                MealEntryModel.date <= end_dt
            ).order_by(MealEntryModel.date).all()
            return [
                MealEntry(
                    id=UUID(m.id),
                    user_id=UUID(m.user_id),
                    product_name=m.product_name,
                    calories=m.calories,
                    date=m.date,
                    created_at=m.created_at
                ) for m in models
            ]
        except Exception as e:
            raise RepositoryError(f"Database error: {e}")