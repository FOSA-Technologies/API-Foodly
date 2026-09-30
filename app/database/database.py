from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import  settings as s

DATABASE_URL = s.db_url


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)


def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()
