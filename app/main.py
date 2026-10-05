from fastapi import FastAPI
# from guard import SecurityConfig, SecurityMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from .database import database
from .database.models import models
from .router import user, role_page, auth, shop
import os
# config = SecurityConfig(
#     enable_rate_limiting=True,
#     rate_limit=2,
#     rate_limit_window=60,
#     enable_ip_banning=True,
#     auto_ban_threshold=5,
#     auto_ban_duration=86400,
#     custom_log_file="security.log",
#     enforce_https=True,
#     enable_cors=True,
#     cors_allow_origins=["https://paulamode.shop", "https://www.paulamode.shop"],
#     cors_allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
#     cors_allow_headers=["*"],
#     cors_allow_credentials=True,
#     cors_expose_headers=["X-Custom-Header"],
#     cors_max_age=600,
#     block_cloud_providers={"AWS", "GCP", "Azure"},
# )
app = FastAPI()
# app.add_middleware(SecurityMiddleware, config=config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://localhost:5174", "https://paulamode.shop", "https://www.paulamode.shop"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs('uploads/customers',exist_ok=True)
os.makedirs('uploads/products',exist_ok=True)
models.Base.metadata.create_all(bind=database.engine)

# app.mount('/app/uploads/customers', StaticFiles(directory="app/uploads/customers"), name="uploads/customers")
# app.mount('/app/uploads/products', StaticFiles(directory="app/uploads/products"), name="uploads/products")
app.include_router(user.router)
app.include_router(role_page.router)
app.include_router(auth.router)
app.include_router(shop.router)
app.get('/')
def root():
    return {"message": "Hello world"}