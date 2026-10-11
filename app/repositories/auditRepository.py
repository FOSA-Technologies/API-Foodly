from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Query, Session

from ..database.models import models


def _escape_like(value: str) -> str:
    """Neutralise % et _ pour que la recherche soit littérale."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class AuditRepository:

    @staticmethod
    def _filtered(db: Session, audit_type: Optional[str] = None, module: Optional[str] = None,
                  user: Optional[str] = None, search: Optional[str] = None,
                  date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> Query:
        query = db.query(models.Audit)
        if audit_type:
            query = query.filter(models.Audit.type == audit_type)
        if module:
            query = query.filter(models.Audit.module == module)
        if user:
            query = query.filter(models.Audit.user_name == user)
        if search:
            pattern = f"%{_escape_like(search.strip())}%"
            query = query.filter(or_(
                models.Audit.message.ilike(pattern, escape="\\"),
                models.Audit.module.ilike(pattern, escape="\\"),
                models.Audit.user_name.ilike(pattern, escape="\\"),
            ))
        if date_from:
            query = query.filter(models.Audit.created_at >= date_from)
        if date_to:
            query = query.filter(models.Audit.created_at <= date_to)
        return query

    @staticmethod
    def _newest_first(query: Query) -> Query:
        return query.order_by(models.Audit.created_at.desc(), models.Audit.id.desc())

    @staticmethod
    def list_page(db: Session, page: int, page_size: int, **filters):
        query = AuditRepository._filtered(db, **filters)
        total = query.count()
        items = (AuditRepository._newest_first(query)
                 .offset((page - 1) * page_size).limit(page_size).all())
        return items, total

    @staticmethod
    def count(db: Session, **filters) -> int:
        return AuditRepository._filtered(db, **filters).count()

    @staticmethod
    def list_all(db: Session, **filters) -> List[models.Audit]:
        return AuditRepository._newest_first(AuditRepository._filtered(db, **filters)).all()

    @staticmethod
    def counts_by_type(db: Session) -> dict:
        rows = db.query(models.Audit.type, func.count(models.Audit.id)).group_by(models.Audit.type).all()
        return {audit_type: count for audit_type, count in rows}

    @staticmethod
    def count_since(db: Session, since: datetime) -> int:
        return db.query(models.Audit).filter(models.Audit.created_at >= since).count()

    @staticmethod
    def distinct_modules(db: Session) -> List[str]:
        rows = db.query(models.Audit.module).distinct().order_by(models.Audit.module).all()
        return [row[0] for row in rows]

    @staticmethod
    def distinct_users(db: Session) -> List[str]:
        rows = db.query(models.Audit.user_name).distinct().order_by(models.Audit.user_name).all()
        return [row[0] for row in rows]