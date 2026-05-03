from uuid import UUID
from ..domain.repositories import UserRepository, ProfileRepository
from ..utils.exceptions import NotFoundError

class UserService:
    def __init__(self, user_repo: UserRepository, profile_repo: ProfileRepository):
        self.user_repo = user_repo
        self.profile_repo = profile_repo

    def get_profile(self, user_id: UUID):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        profile = self.profile_repo.get_by_user_id(user_id)
        result = {"email": user.email}
        if profile:
            result.update({
                "height_cm": profile.height_cm,
                "weight_kg": profile.weight_kg,
                "age": profile.age,
                "gender": profile.gender,
                "daily_calorie_goal": profile.daily_calorie_goal,
            })
        else:
            result.update({
                "height_cm": None,
                "weight_kg": None,
                "age": None,
                "gender": None,
                "daily_calorie_goal": 2000,
            })
        return result

    def update_profile(self, user_id: UUID, **kwargs):
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found")
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        self.profile_repo.save(profile)