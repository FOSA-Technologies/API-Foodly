from random import random
from typing import List

from fastapi import APIRouter, status, HTTPException, Depends,  UploadFile, Form, File
from sqlalchemy.orm import Session
from app.database import database
from app.database.schemas import schemas
from app.database.models import models
from app.utils.utils import upload_pictures
router = APIRouter(prefix='/products', tags = ['Produits'])



@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(depense:int=Form(...), brand:str=Form(...), category_id:int=Form(...), price:int=Form(...), min_stock:int=Form(...), stock:int=Form(...), image: UploadFile=File(None) , db: Session = Depends(database.get_db)):
    check_if_exist_product = db.query(models.Product).filter(models.Product.brand == brand).first()
    if  check_if_exist_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ce produit existe deja")
    check_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not check_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ce category n'existe deja")

    # upload de l'images
    image_url = upload_pictures('app/uploads/', image,['jpg', 'jpeg', 'png'])
    codebar = check_category.category_name+str(int(random())*999999999)
    new_product = models.Product(brand=brand, category_id=category_id, price=price, min_stock=min_stock, stock=stock, image_url=image_url, depense=depense,codebar=codebar)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.get('/', status_code=200, response_model=List[schemas.ProductView])
def get_products(db:Session=Depends(database.get_db)):
    return db.query(models.Product).all()




