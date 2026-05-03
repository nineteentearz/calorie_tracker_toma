# app/services/user_service.py
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
        return {"email": user.email, **profile.__dict__ if profile else {}}

    def update_profile(self, user_id: UUID, **kwargs):
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found")
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        self.profile_repo.save(profile)