from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database.models import models


class TableRepository:

    @staticmethod
    def list_all(db: Session) -> List[models.DiningTable]:
        return db.query(models.DiningTable).order_by(models.DiningTable.id).all()

    @staticmethod
    def get(db: Session, table_id: int) -> Optional[models.DiningTable]:
        return db.get(models.DiningTable, table_id)

    @staticmethod
    def name_exists(db: Session, name: str, ignore_id: Optional[int] = None) -> bool:
        """Unicité sans tenir compte de la casse (même expression que l'index en base)."""
        query = db.query(models.DiningTable.id).filter(
            func.lower(models.DiningTable.table_name) == func.lower(name))
        if ignore_id is not None:
            query = query.filter(models.DiningTable.id != ignore_id)
        return db.query(query.exists()).scalar()
