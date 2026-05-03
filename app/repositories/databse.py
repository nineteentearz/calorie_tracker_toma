from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()