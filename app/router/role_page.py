from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import database
from app.auth import Oauth
from app.database.models import models
from app.database.schemas import schemas
from app.services.auditServices import AuditService

router = APIRouter(tags=["Roles & Pages"])


@router.post('/roles', status_code=status.HTTP_201_CREATED)
def create_role(content: schemas.RoleCreation, db: Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):


    check_role = db.query(models.Role).filter(models.Role.role_name == content.role_name.lower()).first()
    if check_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="le Role existe déjà")

    new_role = models.Role(role_name=content.role_name.lower())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    try:
        for page in content.pages:
            new_roles_pages = models.RolePage(role_id=new_role.id, page_id=page)
            db.add(new_roles_pages)
            db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Impossible de créer le role")

    AuditService.record(db, audit_type="create", module="Paramètres",
                        message=f"Rôle « {new_role.role_name} » créé.", user_id=current_user)
    db.commit()
    return {"message": "Role créée"}

@router.get('/roles', status_code=status.HTTP_200_OK, response_model=List[schemas.RoleData])
def get_all_roles(db: Session = Depends(database.get_db), current_user:int=Depends(Oauth.get_current_user)):
    roles = db.query(models.Role).all()
    return roles


@router.delete('/roles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id:int, db: Session = Depends(database.get_db), current_user:int=Depends(Oauth.get_current_user)):
    query = db.query(models.User).filter(models.User.role_id == id)
    check_used_role = query.first()
    if check_used_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Impossible de supprimer, ce role est actif")

    role_query = db.query(models.Role).filter(models.Role.id == id)
    role = role_query.first()

    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ce role n'existe pas")

    role_name = role.role_name
    role_query.delete(synchronize_session=False)
    AuditService.record(db, audit_type="delete", module="Paramètres",
                        message=f"Rôle « {role_name} » supprimé.", user_id=current_user)
    db.commit()

    return {"message": "Role supprimé"}




@router.post("/pages", status_code=status.HTTP_201_CREATED)
def create_pages(content: schemas.PageCreation, db: Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):
    check_page = db.query(models.Page).filter(models.Page.page_path == content.page_path).first()
    if check_page:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette page existe déjà")

    new_page = models.Page(**content.model_dump())
    db.add(new_page)
    AuditService.record(db, audit_type="create", module="Paramètres",
                        message=f"Page « {content.page_name} » créée.", user_id=current_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette page existe déjà")
    db.refresh(new_page)
    return {"message":"Page créée"}


@router.get('/pages', status_code=status.HTTP_200_OK, response_model=List[schemas.Page], )
def get_pages(db: Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):
    return db.query(models.Page).all()


@router.delete('/pages/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_page(id: int, db: Session = Depends(database.get_db), current_user= Depends(
    Oauth.get_current_user)):
    page = db.query(models.Page).filter(models.Page.id == id).first()
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette page n'existe pas")

    check_used_page = db.query(models.RolePage).filter(models.RolePage.page_id == id).first()
    if check_used_page:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Impossible de supprimer, cette page est utilisée par un rôle")

    page_name = page.page_name
    db.delete(page)
    AuditService.record(db, audit_type="delete", module="Paramètres",
                        message=f"Page « {page_name} » supprimée.", user_id=current_user)
    db.commit()