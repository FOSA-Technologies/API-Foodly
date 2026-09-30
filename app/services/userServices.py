
from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.utils import utils
from app.database.models import models
from app.repositories.userRepository import  UserRepository
from app.database.schemas import schemas


class UserService:

    # Creation d'un utilisateur
    @staticmethod
    def create_user(content:schemas.UserCreation, db: Session):
        check_user =  UserRepository.find_user_by_email(content.email, db)
        if check_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="L'utilisateur existe déjà")
        # A refactoriser pour plus tard
        check_role = db.query(models.Role).filter(models.Role.id == content.role_id).first()
        if not check_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="le Role n'existe pas")
        new_user = models.User(**content.model_dump())
        hashed_password = utils.hash_password(new_user.password)
        new_user.password = hashed_password
        UserRepository.add(new_user, db)
        return {"message": "Utilisateur créée"}


    # Verification si utilisateur
    @staticmethod
    def get_user(current_user:int, db:Session) -> schemas.UserData:
        check_user = UserRepository.find_user_by_id(current_user, db)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentials ")
        return check_user

    # Recuperation de tout les utilisateurs
    @staticmethod
    def get_all_users(db: Session) -> List[schemas.UserInfo]:
        return UserRepository.get_all_users(db)

    #
    # @staticmethod
    # def update_user(content: schemas.UserStatus, db:Session):
    #     check_user = UserRepository.