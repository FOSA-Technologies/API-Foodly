import csv
import io
from datetime import UTC, datetime, timedelta
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from ..database.models import models

MAX_MESSAGE_LENGTH = 500
# Nombre maximum de lignes d'un export CSV (au-delà, il faut affiner les filtres)
EXPORT_LIMIT = 50_000

TYPE_LABELS = {
    "create": "Ajout",
    "update": "Modification",
    "delete": "Suppression",
    "sale": "Vente",
    "login": "Connexion",
}

# Un tableur interprète une cellule commençant par ces caractères comme une formule
_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


class AuditService:

    @staticmethod
    def record(db: Session, *, audit_type: str, module: str, message: str,
               user_id: Optional[int] = None) -> models.Audit:
        """
        Ajoute une ligne au journal dans la transaction en cours : elle est validée (ou annulée)
        avec l'action qu'elle décrit, donc l'appelant doit faire db.commit() ensuite.
        Sans utilisateur connu, l'action est attribuée à « Système ».
        """
        user = db.get(models.User, user_id) if user_id is not None else None
        if len(message) > MAX_MESSAGE_LENGTH:
            message = message[:MAX_MESSAGE_LENGTH - 1] + "…"

        audit = models.Audit(
            type=audit_type,
            module=module,
            message=message,
            user_id=user.id if user else None,
            user_name=user.username if user else "Système",
            user_role=(user.role.role_name if user.role else "—") if user else "—",
        )
        db.add(audit)
        return audit

    @staticmethod
    def _cell(value: str) -> str:
        return f"'{value}" if value.startswith(_FORMULA_PREFIXES) else value

    @staticmethod
    def to_csv(rows: Iterable[models.Audit], utc_offset_minutes: int = 0) -> str:
        """CSV séparé par « ; » (ouvre correctement dans Excel en français). Dates en heure locale."""
        buffer = io.StringIO()
        out = csv.writer(buffer, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        out.writerow(["Date", "Type", "Module", "Explication", "Utilisateur", "Rôle"])
        shift = timedelta(minutes=utc_offset_minutes)
        for row in rows:
            local = row.created_at.astimezone(UTC) + shift
            out.writerow([AuditService._cell(value) for value in (
                local.strftime("%d/%m/%Y %H:%M"),
                TYPE_LABELS.get(row.type, row.type),
                row.module,
                row.message,
                row.user_name,
                row.user_role,
            )])
        return buffer.getvalue()

    @staticmethod
    def start_of_today_utc() -> datetime:
        return datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)