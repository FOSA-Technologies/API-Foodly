
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import database
from app.auth import Oauth
from app.database.models import models
from app.database.schemas import schemas
from app.repositories.userRepository import UserRepository
from app.services.userServices import  UserService
router = APIRouter(tags=["Users"], prefix='/users')

@router.post('/')
def create_user(content: schemas.UserCreation, db: Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):
    return UserService.create_user(content, db)



@router.get('/current', status_code=status.HTTP_200_OK, response_model=schemas.UserData)
def get_user(db:Session = Depends(database.get_db), current_user= Depends(Oauth.get_current_user)):
    return UserService.get_user(current_user, db)



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserInfo])
def get_all_users(db:Session = Depends(database.get_db), current_user= Depends(Oauth.get_current_user)):
    return UserService.get_all_users(db)


@router.patch('/', status_code=status.HTTP_202_ACCEPTED)
def change_user_status(content: schemas.UserStatus, db:Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == content.user_id)
    user =  UserRepository.find_user_by_id(content.user_id, db)
    user_query.update({"active": not user.active})
    db.commit()
    return {"message": f"Compte {"activé" if user.active else "désactivé"}"}


# modication information utilisateur
@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id:int, content:schemas.UserInfo, db:Session=Depends(database.get_db)):
    query = db.query(models.User).filter(models.User.id == user_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisation introuvable")
    # verification si email existe deja
    exist_email = db.query(models.User).filter(models.User.email == content.email, models.User.id != user_id).first()
    if exist_email:
        raise HTTPException(status_code=400, detail="Cet email existe déjà")
    query.update(content.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": "Information modifié"}
    
