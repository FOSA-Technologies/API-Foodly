from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ForeignKey, Text, Numeric, UUID, CheckConstraint, Float, BigInteger, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Relationship

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String(100), nullable=False)
    pages = relationship('Page', secondary='roles_pages', back_populates="roles")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True, nullable=False)
    page_name = Column(String(100), nullable=False)
    page_path = Column(String(50), nullable=False, unique=True)
    roles = relationship('Role', secondary='roles_pages', back_populates="pages")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class RolePage(Base):
    __tablename__ = "roles_pages"
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, server_default="true")
    role_id = Column(Integer, ForeignKey('roles.id', ondelete="CASCADE"), nullable=False)
    role = relationship('Role')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Shop(Base):
    """Informations de la boutique : une seule ligne (id = 1)."""
    __tablename__ = "shop_settings"
    __table_args__ = (CheckConstraint("id = 1", name="shop_settings_single_row"),)
    id = Column(Integer, primary_key=True, nullable=False)
    shop_name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    currency = Column(String(3), nullable=False)
    tax_rate = Column(Numeric(5, 2), nullable=False)



class Category(Base):
    __tablename__ = "categories"
    id= Column(Integer, primary_key=True, nullable=False)
    color_hex = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    products = Relationship('Product', back_populates='category')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


# pour les produits
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    codebar = Column(String(250), nullable=True)
    brand = Column(String(50), nullable=False)
    stock = Column(Integer, nullable=False)
    min_stock = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    price = Column(Float, nullable= False )
    depense = Column(Float, nullable = False)
    category = Relationship('Category', back_populates='products')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

class Audit(Base):
    """Journal d'audit : une ligne par action effectuée sur la plateforme (jamais modifiée)."""
    __tablename__ = "audits"
    __table_args__ = (
        CheckConstraint("type IN ('create', 'update', 'delete', 'sale', 'login')", name="audits_type_check"),
        Index("ix_audits_created_at", "created_at"),
        Index("ix_audits_type", "type"),
        Index("ix_audits_module", "module"),
        Index("ix_audits_user_name", "user_name"),
    )
    id = Column(BigInteger, primary_key=True, nullable=False)
    type = Column(String(10), nullable=False)
    module = Column(String(50), nullable=False)
    message = Column(String(500), nullable=False)
    # L'utilisateur est copié (nom + rôle) pour que l'historique reste lisible
    # même si le compte est modifié ou supprimé par la suite.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_name = Column(String(100), nullable=False)
    user_role = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))