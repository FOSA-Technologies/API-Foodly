from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.orm import Session

from app.database import database
from app.utils import utils
from app.auth import Oauth
from app.database.models import models
from app.database.schemas import schemas

router = APIRouter(tags=['Authentification'])


@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login(content: schemas.UserLogin, db: Session = Depends(database.get_db)):
    check_user = db.query(models.User).filter(models.User.email == content.email).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalide email ou mot de passe")

    if not utils.verify_password(content.password, check_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalide email ou mot de passe")

    if not check_user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Compte non activé")

    return Oauth.create_access_token({"user_id": check_user.id})