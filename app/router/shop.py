from fastapi import APIRouter, Depends, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.auth import Oauth
from app.database import database
from app.database.models import models
from app.database.schemas import schemas

router = APIRouter(tags=["Shop"])

# Valeurs renvoyées tant que la boutique n'a jamais été configurée
DEFAULT_SHOP = {"shop_name": "", "city": "", "currency": "MAD", "tax_rate": 0}


@router.get('/shop', status_code=status.HTTP_200_OK, response_model=schemas.ShopSettings)
def get_shop(db: Session = Depends(database.get_db), current_user=Depends(Oauth.get_current_user)):
    shop = db.get(models.Shop, 1)
    if not shop:
        return schemas.ShopSettings(**DEFAULT_SHOP)
    return shop


@router.put('/shop', status_code=status.HTTP_200_OK, response_model=schemas.ShopSettings)
def update_shop(content: schemas.ShopSettingsUpdate, db: Session = Depends(database.get_db),
                current_user=Depends(Oauth.get_current_user)):
    values = content.model_dump()
    # Création ou mise à jour en une seule requête (la ligne a toujours l'id 1)
    stmt = insert(models.Shop).values(id=1, **values).on_conflict_do_update(
        index_elements=[models.Shop.id], set_=values)
    db.execute(stmt)
    db.commit()
    return db.get(models.Shop, 1)
