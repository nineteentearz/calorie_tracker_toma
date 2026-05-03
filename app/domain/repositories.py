from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import date
from .models import User, Profile, MealEntry

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: ...
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]: ...

class ProfileRepository(ABC):
    @abstractmethod
    def save(self, profile: Profile) -> None: ...
    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> Optional[Profile]: ...

class MealEntryRepository(ABC):
    @abstractmethod
    def add(self, entry: MealEntry) -> None: ...
    @abstractmethod
    def get_by_user_and_date_range(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> List[MealEntry]: ...