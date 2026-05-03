from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True

@dataclass
class Profile:
    user_id: UUID
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    daily_calorie_goal: int = 2000
    updated_at: datetime = None

@dataclass
class MealEntry:
    id: UUID
    user_id: UUID
    product_name: str
    calories: int
    date: datetime
    created_at: datetime