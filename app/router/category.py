from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database.schemas import schemas
from app.database.models import models
from app.database import database
from app.auth import Oauth
router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(content: schemas.CategoryCreate, db: Session = Depends(database.get_db),  current_user:int=Depends(Oauth.get_current_user)):
    is_unique  = db.query(models.Category).filter(models.Category.category_name == content.category_name).first()
    if is_unique:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cette categorie existe déjà")

    new_category = models.Category(**content.model_dump())
    db.add(new_category)
    db.commit()
    return {"message": "Categorie créée"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Category])
def get_all(db: Session = Depends(database.get_db), current_user:int=Depends(Oauth.get_current_user)):
    return db.query(models.Category).all()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id:int, db:Session=Depends(database.get_db), current_user:int=Depends(Oauth.get_current_user)):
    query = db.query(models.Category).filter(models.Category.id == id)
    category = query.first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categorie non trouvé")
    query.delete(synchronize_session=False)
    db.commit()
    return {"message":"Categorie supprimé"}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_category(id:int, content: schemas.CategoryCreate,  db:Session=Depends(database.get_db), current_user:int=Depends(Oauth.get_current_user)):
    query = db.query(models.Category).filter(models.Category.id == id)
    category = query.first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categorie non trouvé")
    query.update(content.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": "Categorie modifié"}

