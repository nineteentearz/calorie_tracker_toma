"""
Контроллеры для связи GUI с бизнес-логикой.
"""
import logging
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from uuid import UUID

from ..repositories.database import SessionLocal
from ..repositories.sqlalchemy_repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyProfileRepository,
    SQLAlchemyMealEntryRepository,
    SQLAlchemyProductRepository
)
from ..services.auth_service import AuthService
from ..services.user_service import UserService
from ..services.calorie_service import CalorieService
from ..services.progress_service import ProgressService
from ..services.product_service import ProductService
from ..utils.session import save_current_user_id, get_current_user_id, clear_session
from ..utils.exceptions import (
    AuthenticationError, UserAlreadyExistsError,
    NotFoundError, ValidationError, RepositoryError
)

logger = logging.getLogger(__name__)


class AppController:
    """Главный контроллер, инициализирует все сервисы и управляет сессией."""

    def __init__(self):
        self.db_session = SessionLocal()
        self.user_repo = SQLAlchemyUserRepository(self.db_session)
        self.profile_repo = SQLAlchemyProfileRepository(self.db_session)
        self.meal_repo = SQLAlchemyMealEntryRepository(self.db_session)
        self.product_repo = SQLAlchemyProductRepository(self.db_session)

        self.auth_service = AuthService(self.user_repo, self.profile_repo)
        self.user_service = UserService(self.user_repo, self.profile_repo)
        self.calorie_service = CalorieService(self.meal_repo)
        self.progress_service = ProgressService(self.meal_repo, self.profile_repo)
        self.product_service = ProductService(self.product_repo)

        self._current_user_id: Optional[UUID] = None

    def login(self, email: str, password: str) -> bool:
        """Пытается авторизовать пользователя. Возвращает True при успехе."""
        try:
            user = self.auth_service.login(email, password)
            self._current_user_id = user.id
            save_current_user_id(user.id)
            return True
        except AuthenticationError as e:
            logger.warning(f"Login failed for {email}: {e}")
            return False

    def register(self, email: str, password: str) -> bool:
        """Регистрирует нового пользователя. Возвращает True при успехе."""
        try:
            self.auth_service.register(email, password)
            return True
        except UserAlreadyExistsError as e:
            logger.warning(f"Registration failed: {e}")
            return False

    def logout(self):
        """Завершает сеанс."""
        self._current_user_id = None
        clear_session()

    def is_authenticated(self) -> bool:
        """Проверяет, есть ли активная сессия (при запуске)."""
        user_id = get_current_user_id()
        if user_id:
            user = self.user_repo.get_by_id(user_id)
            if user:
                self._current_user_id = user_id
                return True
        return False

    def get_current_user_id(self) -> Optional[UUID]:
        return self._current_user_id

    # --- Методы для работы с профилем ---
    def get_profile(self) -> Dict[str, Any]:
        """Возвращает профиль текущего пользователя."""
        if not self._current_user_id:
            raise AuthenticationError("Not logged in")
        return self.user_service.get_profile(self._current_user_id)

    def update_profile(self, **kwargs) -> bool:
        """Обновляет поля профиля. Возвращает True при успехе."""
        if not self._current_user_id:
            return False
        try:
            self.user_service.update_profile(self._current_user_id, **kwargs)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Profile update error: {e}")
            return False

    # --- Методы для работы с приёмами пищи ---
    def add_meal(self, product_name: str, calories: int, meal_date: date) -> bool:
        """Добавляет запись о приёме пищи."""
        if not self._current_user_id:
            return False
        try:
            from ..domain.models import MealEntry
            from uuid import uuid4
            entry = MealEntry(
                id=uuid4(),
                user_id=self._current_user_id,
                product_name=product_name,
                calories=calories,
                date=datetime.combine(meal_date, datetime.min.time()),
                created_at=datetime.utcnow()
            )
            self.meal_repo.add(entry)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Add meal error: {e}")
            return False

    def get_calories_for_range(self, start_date: date, end_date: date) -> List[Dict]:
        """Возвращает список словарей {date, total_calories} для диапазона."""
        if not self._current_user_id:
            return []
        return self.calorie_service.get_calories_by_date_range(
            self._current_user_id, start_date, end_date
        )

    def get_daily_progress(self, target_date: date) -> Optional[Dict]:
        """Возвращает прогресс за указанный день."""
        if not self._current_user_id:
            return None
        try:
            return self.progress_service.get_daily_progress(self._current_user_id, target_date)
        except NotFoundError:
            return None

    def set_daily_goal(self, goal: int) -> bool:
        """Устанавливает новую дневную цель калорий."""
        if not self._current_user_id:
            return False
        try:
            self.progress_service.update_goal(self._current_user_id, goal)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Set goal error: {e}")
            return False

    # --- Методы для работы с продуктами ---
    def get_all_products(self):
        """Возвращает список всех продуктов."""
        if not self._current_user_id:
            return []
        return self.product_service.get_all_products()

    def create_product(self, name: str, calories: int):
        """Создаёт новый продукт."""
        return self.product_service.create_product(name, calories)

    def update_product(self, product_id: UUID, name: str, calories: int):
        """Обновляет существующий продукт."""
        return self.product_service.update_product(product_id, name, calories)

    def delete_product(self, product_id: UUID):
        """Удаляет продукт."""
        self.product_service.delete_product(product_id)

    def close(self):
        """Закрывает сессию БД при завершении приложения."""
        self.db_session.close()