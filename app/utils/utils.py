from time import time
from typing import List

from fastapi import UploadFile
from pwdlib import PasswordHash
from app.config.config import settings
from fastapi import HTTPException, status
password_context = PasswordHash.recommended()
import os
import shutil

def hash_password(plaintext:str):
    return password_context.hash(plaintext)


def verify_password(plaintext:str, hashed):
    return password_context.verify(plaintext, hashed)


# pour gérer les uploads d'images dynamiquement
def upload_pictures(public_path:str, image:UploadFile|None, allow_file_extension:List[str])->str:
    os.makedirs(public_path, exist_ok=True)
    try:
        if image:

            file = image.file
            filename = image.filename
            image_ext = str(filename).split('.')[-1]
            if image_ext not in allow_file_extension:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Fichier non pris en charge (ex: jpeg, png, jpg)")
            new_filename = str(time()) + "." + image_ext
            filepath = os.path.join(public_path, new_filename)
            with open(filepath, "wb") as f:
                
                shutil.copyfileobj(file, f)
            return f"{settings.api_url}/" + filepath
        else:
            return os.path.join(f"{settings.api_url}/" + public_path, "/default.png")

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="impossible d'importer l'image")



# Gérer l'auto suppression d'une image ancien lors de modification d'un article
def remove_old_pictures(image:UploadFile, old_image:str):
    if image is not None:
        if os.path.exists(old_image[len(f"{settings.api_url}/"):]):
            os.remove(old_image[len(f"{settings.api_url}/"):])


# Gérer l'auto suppression d'une image
def remove_pictures(image:str):
    if os.path.exists(image[len(f"{settings.api_url}/"):]):
            os.remove(image[len(f"{settings.api_url}/"):])
