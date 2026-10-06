import uuid
from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, StringConstraints
from sqlalchemy import Boolean, Uuid


class User(BaseModel):
    username:str
    email:EmailStr
    password:str


class UserCreation(BaseModel):
    username:str
    email:EmailStr
    password:str
    role_id:int

class UserLogin(BaseModel):
    email:EmailStr
    password:str




class Role(BaseModel):
    id:int
    role_name:str
    created_at:datetime

class RoleCreation(BaseModel):
    role_name:str
    pages:List[int]

class PageCreation(BaseModel):
    page_name:str
    page_path:str


# doit faire une refactorisation ici peut etre plutard
class RoleData(BaseModel):
    id: int
    role_name: str
    pages: List[PageCreation]






class UserData(BaseModel):
    id:int
    username:str
    email:str
    role:RoleData


class RoleName(BaseModel):
    role_name:str


class UserInfo(BaseModel):
    id:int
    username:str
    email:str
    active:bool
    role:RoleName
    created_at:datetime

class UserStatus(BaseModel):
    user_id:int

class Page(BaseModel):
    id:int
    page_name:str
    page_path:str
    created_at:datetime


class CustomerView(BaseModel):
    id:int
    client_name:str
    notes:Optional[str]=''
    phone:int
    cin:int
    picture_url:str
    is_promoted:bool
    is_reseller: bool
    total_purchases: int
    total_invoices: int
    created_at:datetime


class CustomerCreation(BaseModel):
    client_name:str
    notes:str
    phone:int
    cin:int



class CustomerNotes(BaseModel):
    notes: Optional[str] = ''


class Shop(BaseModel):
    shop_name:str
    devise:str
    tva:int
    id: uuid.UUID


class ShopCreate(BaseModel):
    shop_name:str
    devise:str
    tva:int 


class Category(BaseModel):
    id:int
    category_name:str
    color_hex:str
    created_at: datetime


class CategoryCreate(BaseModel):
    category_name:str
    color_hex:str


class Genre(BaseModel):
    id:int
    genre_name:str
    created_at: datetime


class GenreCreate(BaseModel):
    genre_name:str


class Size(BaseModel):
    id:int
    size_name: str
    created_at:datetime


class Color(BaseModel):
    id:int
    color_name: str
    hex:str
    created_at:datetime


class SizeCreate(BaseModel):
    size_name:str


class StockCreate(BaseModel):
    size_id:int
    color_id:int
    product_id:int
    count:int

class StockView(StockCreate):
    pass

class StockAdd(BaseModel):
    size_id: int
    color_id: int
    count: int


class ProductsSizes(BaseModel):
    product_id:int
    size_id:int
    color_id:int


class ProductsColors(BaseModel):
    product_id:int
    color_id:int


class ColorCreate(BaseModel):
    color_name:str
    hex:str


class ProductCreate(BaseModel):
    brand:str
    category_id:int
    genre_id:int
    description:str
    price:int
    min_stock:int


class Variants(BaseModel):
    color_id:int
    size_id:int
    stock:int


class VariantsEdit(BaseModel):
    color_id:int
    size_id:int
    count:int


class Product(BaseModel):
    id:int
    brand:str
    description:str
    price:int
    is_new:bool
    image_url:str
    code:str
    is_available:bool
    colors:List[Color]
    sizes:List[Size]
    min_stock:int
    stocks: List[StockView]


class ProductEdit(BaseModel):
    id:int
    brand:str
    description:str
    price:int
    is_new:bool
    image_url:str
    is_available:bool
    genre_id:int
    purchase_price:int
    min_stock:int


class ProductShow(BaseModel):
    product:Product
    count:int


class AddSStock(BaseModel):
    id:int
    variants:str


class UpdateProduct(BaseModel):
    brand:str
    description:str
    price:int
    is_new:bool
    image_url:str
    is_available:bool
    genre_id:int
    purchase_price:int
    min_stock: int



class SupplierCreate(BaseModel):
    supplier_name:Optional[str]="None"
    company:str
    email:Optional[str]="None"
    tel: Optional[int]="000000"


class SupplierShow(BaseModel):
    id:int
    supplier_name:str
    company:str
    email:str
    tel: int


class SupplierEdit(BaseModel):
    supplier_name:str
    company:str
    email:str
    tel:int


class PortfolioCreate(BaseModel):
    portfolio_name: str


class PortfolioView(BaseModel):
    id:int
    portfolio_name:str
    balance:int


class StockMouvementCreate(BaseModel):
    quantity:int
    supplier_id:int
    unit_cost:int
    size_id:int
    color_id:int
    product_id:int
    portfolio_id:int
    received_at:datetime


class ColorName(BaseModel):
    color_name:str


class SupplierName(BaseModel):
    supplier_name:str


class SizeName(BaseModel):
    size_name:str


class PortfolioName(BaseModel):
    portfolio_name:str


class ProductName(BaseModel):
    brand:str


class  StockMouvementShow(BaseModel):
    supplier:SupplierName
    # color:ColorName
    # size:SizeName
    portfolio:PortfolioName
    product:ProductName
    received_at:datetime
    unit_cost: int
    total_cost:int
    quantity:int
    created_at:datetime


class TransactionCreation(BaseModel):

    p_from:int
    p_to:int
    amount:int
    motif:str
    date:str


class TransactionHistory(BaseModel):
    id:int
    p_from:int
    p_to:int
    amount:int
    motif:str
    date:str
    portfolio_from: PortfolioView
    portfolio_to: PortfolioView
    created_at:datetime


class PortfolioSupply(BaseModel):
    portfolio_id:int
    amount:int
    date: str


class PortfolioSupplyHistoryCreation(BaseModel):
    amount:int
    portfolio_id:int
    date:str


ShopText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class ShopSettingsUpdate(BaseModel):
    shop_name: ShopText
    city: ShopText
    currency: str = Field(pattern=r"^[A-Z]{3}$")  # code ISO 4217 : MAD, EUR, USD, MGA...
    tax_rate: float = Field(ge=0, le=100)


class ShopSettings(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    shop_name: str
    city: str
    currency: str
    tax_rate: float