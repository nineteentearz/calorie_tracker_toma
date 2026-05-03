from uuid import uuid4
from datetime import datetime
from ..domain.models import User, Profile
from ..domain.repositories import UserRepository, ProfileRepository
from ..utils.security import hash_password, verify_password
from ..utils.exceptions import AuthenticationError, UserAlreadyExistsError

class AuthService:
    def __init__(self, user_repo: UserRepository, profile_repo: ProfileRepository):
        self.user_repo = user_repo
        self.profile_repo = profile_repo

    def register(self, email: str, password: str) -> User:
        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsError(f"User with email {email} already exists")
        hashed = hash_password(password)
        user = User(
            id=uuid4(),
            email=email,
            hashed_password=hashed,
            created_at=datetime.utcnow()
        )
        self.user_repo.add(user)
        profile = Profile(
            user_id=user.id,
            daily_calorie_goal=2000,
            updated_at=datetime.utcnow()
        )
        self.profile_repo.save(profile)
        return user

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        return user