class CalorieTrackerError(Exception):
    pass

class UserAlreadyExistsError(CalorieTrackerError):
    pass

class AuthenticationError(CalorieTrackerError):
    pass

class NotFoundError(CalorieTrackerError):
    pass

class ValidationError(CalorieTrackerError):
    pass

class RepositoryError(CalorieTrackerError):
    pass