from typing import List
from sqlalchemy.orm import Session
from app.database.schemas import schemas
from ..database.models import models


class UserRepository:


    @staticmethod
    def  find_user_by_id(user_id:int, db: Session):
        return (
            db.query(models.User).filter(models.User.id == user_id).first()
        )


    @staticmethod
    def  find_user_by_email(email:str, db: Session):
        return (
            db.query(models.User).filter(models.User.email == email).first()
        )


    @staticmethod
    def add(content: models.User, db: Session):
        db.add(content)
        db.commit()


    @staticmethod
    def get_all_users(db: Session) -> List[schemas.UserInfo]:
        return db.query(models.User).all()



    # @staticmethod
    # def update_user(content: dict, db: Session):
    #     db.query(models.User).filter(models.User.id == content["id"]).update(content, synchronize_session=False)
    #     db.commit()