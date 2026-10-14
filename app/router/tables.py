from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth import Oauth
from app.database import database
from app.database.schemas import schemas
from app.repositories.tableRepository import TableRepository
from app.services.tableServices import TableService

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("", response_model=List[schemas.TableData], status_code=status.HTTP_200_OK)
@router.get("/", response_model=List[schemas.TableData], status_code=status.HTTP_200_OK, include_in_schema=False)
def get_all(db: Session = Depends(database.get_db), current_user: int = Depends(Oauth.get_current_user)):
    return TableRepository.list_all(db)


@router.post("", response_model=schemas.TableData, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=schemas.TableData, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_table(content: schemas.TableCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(Oauth.get_current_user)):
    return TableService.create(db, content, user_id=current_user)


@router.put("/{id}", response_model=schemas.TableData, status_code=status.HTTP_200_OK)
def update_table(id: int, content: schemas.TableCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(Oauth.get_current_user)):
    return TableService.update(db, id, content, user_id=current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(id: int, db: Session = Depends(database.get_db),
                 current_user: int = Depends(Oauth.get_current_user)):
    TableService.delete(db, id, user_id=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
