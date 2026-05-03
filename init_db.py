# init_db.py
from app.repositories.database import engine, Base
from app.repositories.orm_models import UserModel, ProfileModel, MealEntryModel

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")