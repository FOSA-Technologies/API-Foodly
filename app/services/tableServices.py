from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database.models import models
from ..database.schemas import schemas
from ..repositories.tableRepository import TableRepository
from .auditServices import AuditService

MODULE = "Tables"

STATUS_LABELS = {
    "free": "Libre",
    "occupied": "Occupée",
    "reserved": "Réservée",
    "cleaning": "Nettoyage",
}

NAME_TAKEN = "Une table porte déjà ce nom."
NOT_FOUND = "Table introuvable."


class TableService:

    @staticmethod
    def _normalize(payload: schemas.TableCreate) -> dict:
        """Garde des données cohérentes : convives seulement si occupée, pas de note si libre/nettoyage."""
        values = payload.model_dump()
        if values["status"] != "occupied":
            values["guests"] = None
        if values["status"] in ("free", "cleaning"):
            values["info"] = None
        else:
            values["info"] = values["info"] or None
        return values

    @staticmethod
    def _ensure_name_available(db: Session, name: str, ignore_id: Optional[int] = None) -> None:
        if TableRepository.name_exists(db, name, ignore_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=NAME_TAKEN)

    @staticmethod
    def _commit(db: Session) -> None:
        """Valide la transaction ; un doublon de nom concurrent (index unique) devient une erreur 409."""
        try:
            db.commit()
        except IntegrityError as error:
            db.rollback()
            if "uq_dining_tables_name_lower" in str(error.orig):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=NAME_TAKEN)
            raise

    @staticmethod
    def _get_or_404(db: Session, table_id: int) -> models.DiningTable:
        table = TableRepository.get(db, table_id)
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return table

    @staticmethod
    def create(db: Session, payload: schemas.TableCreate, user_id: int) -> models.DiningTable:
        values = TableService._normalize(payload)
        TableService._ensure_name_available(db, values["table_name"])

        table = models.DiningTable(**values)
        db.add(table)
        AuditService.record(db, audit_type="create", module=MODULE, user_id=user_id,
                            message=f"Table « {values['table_name']} » ajoutée ({values['capacity']} places).")
        TableService._commit(db)
        db.refresh(table)
        return table

    @staticmethod
    def update(db: Session, table_id: int, payload: schemas.TableCreate, user_id: int) -> models.DiningTable:
        table = TableService._get_or_404(db, table_id)
        values = TableService._normalize(payload)
        TableService._ensure_name_available(db, values["table_name"], ignore_id=table_id)

        # Rien n'a changé : pas d'écriture et pas de ligne d'audit inutile
        if all(getattr(table, key) == value for key, value in values.items()):
            return table

        old_name = table.table_name
        renamed = old_name != values["table_name"]
        status_only = (not renamed
                       and table.zone == values["zone"]
                       and table.capacity == values["capacity"]
                       and table.status != values["status"])

        if renamed:
            message = f"Table « {old_name} » renommée en « {values['table_name']} »."
        elif status_only:
            message = f"Table « {old_name} » passée en « {STATUS_LABELS[values['status']]} »."
        else:
            message = f"Table « {old_name} » mise à jour."

        for key, value in values.items():
            setattr(table, key, value)
        AuditService.record(db, audit_type="update", module=MODULE, message=message, user_id=user_id)
        TableService._commit(db)
        db.refresh(table)
        return table

    @staticmethod
    def delete(db: Session, table_id: int, user_id: int) -> None:
        table = TableService._get_or_404(db, table_id)
        name = table.table_name
        db.delete(table)
        AuditService.record(db, audit_type="delete", module=MODULE, user_id=user_id,
                            message=f"Table « {name} » supprimée.")
        db.commit()
