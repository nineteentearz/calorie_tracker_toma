from datetime import date, timedelta
from uuid import UUID
from collections import defaultdict
from ..domain.repositories import MealEntryRepository

class CalorieService:
    def __init__(self, meal_repo: MealEntryRepository):
        self.meal_repo = meal_repo

    def get_calories_by_date_range(self, user_id: UUID, start: date, end: date):
        entries = self.meal_repo.get_by_user_and_date_range(user_id, start, end)
        agg = defaultdict(int)
        for e in entries:
            agg[e.date.date()] += e.calories
        result = []
        current = start
        while current <= end:
            result.append({
                "date": current.isoformat(),
                "total_calories": agg.get(current, 0)
            })
            current += timedelta(days=1)
        return result