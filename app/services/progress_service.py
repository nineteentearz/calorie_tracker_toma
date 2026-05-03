# app/services/progress_service.py
from datetime import date, timedelta
from uuid import UUID
from ..domain.repositories import MealEntryRepository, ProfileRepository
from ..utils.exceptions import NotFoundError

class ProgressService:
    def __init__(self, meal_repo: MealEntryRepository, profile_repo: ProfileRepository):
        self.meal_repo = meal_repo
        self.profile_repo = profile_repo

    def get_daily_progress(self, user_id: UUID, target_date: date):
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found")
        entries = self.meal_repo.get_by_user_and_date_range(
            user_id, target_date, target_date
        )
        total = sum(e.calories for e in entries)
        goal = profile.daily_calorie_goal
        percent = (total / goal * 100) if goal > 0 else 0
        return {
            "date": target_date,
            "total_calories": total,
            "daily_goal": goal,
            "percentage": round(percent, 2)
        }

    def update_goal(self, user_id: UUID, new_goal: int):
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found")
        profile.daily_calorie_goal = new_goal
        self.profile_repo.save(profile)