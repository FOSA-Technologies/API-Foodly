import math
from datetime import UTC, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.auth import Oauth
from app.database import database
from app.database.schemas import schemas
from app.repositories.auditRepository import AuditRepository
from app.services.auditServices import AuditService, EXPORT_LIMIT

router = APIRouter(tags=["Audits"], prefix="/audits")

AUDIT_TYPES = ["create", "update", "delete", "sale", "login"]


def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Une date sans fuseau est considérée comme UTC."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def audit_filters(
        audit_type: Optional[schemas.AuditType] = Query(None, alias="type"),
        module: Optional[str] = Query(None, max_length=50),
        user: Optional[str] = Query(None, max_length=100, description="Nom de l'utilisateur"),
        search: Optional[str] = Query(None, max_length=200, description="Cherche dans l'explication, le module et l'utilisateur"),
        date_from: Optional[datetime] = Query(None, description="Début (inclus), ISO 8601"),
        date_to: Optional[datetime] = Query(None, description="Fin (incluse), ISO 8601"),
) -> dict:
    date_from, date_to = _as_utc(date_from), _as_utc(date_to)
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="La date de début doit précéder la date de fin")
    return {
        "audit_type": audit_type,
        "module": module or None,
        "user": user or None,
        "search": search or None,
        "date_from": date_from,
        "date_to": date_to,
    }


@router.get("", response_model=schemas.AuditPage, status_code=status.HTTP_200_OK)
@router.get("/", response_model=schemas.AuditPage, status_code=status.HTTP_200_OK, include_in_schema=False)
def list_audits(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        filters: dict = Depends(audit_filters),
        db: Session = Depends(database.get_db),
        current_user: int = Depends(Oauth.get_current_user)):
    items, total = AuditRepository.list_page(db, page, page_size, **filters)
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": max(1, math.ceil(total / page_size)),
    }


@router.post("", response_model=schemas.AuditData, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=schemas.AuditData, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_audit(content: schemas.AuditCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(Oauth.get_current_user)):
    # L'auteur vient toujours du token, jamais du corps de la requête
    audit = AuditService.record(db, audit_type=content.type, module=content.module,
                                message=content.message, user_id=current_user)
    db.commit()
    db.refresh(audit)
    return audit


@router.get("/stats", response_model=schemas.AuditStats, status_code=status.HTTP_200_OK)
def audit_stats(
        since: Optional[datetime] = Query(None, description="Début de « aujourd'hui » (ISO 8601). Par défaut : minuit UTC"),
        db: Session = Depends(database.get_db),
        current_user: int = Depends(Oauth.get_current_user)):
    counts = AuditRepository.counts_by_type(db)
    since = _as_utc(since) or AuditService.start_of_today_utc()
    return {
        "total": sum(counts.values()),
        "today": AuditRepository.count_since(db, since),
        "by_type": {audit_type: counts.get(audit_type, 0) for audit_type in AUDIT_TYPES},
    }


@router.get("/filters", response_model=schemas.AuditFilters, status_code=status.HTTP_200_OK)
def audit_filter_values(db: Session = Depends(database.get_db),
                        current_user: int = Depends(Oauth.get_current_user)):
    """Valeurs disponibles pour les listes déroulantes de filtres."""
    return {
        "types": AUDIT_TYPES,
        "modules": AuditRepository.distinct_modules(db),
        "users": AuditRepository.distinct_users(db),
    }


@router.get("/export", status_code=status.HTTP_200_OK)
def export_audits(
        utc_offset: int = Query(0, ge=-840, le=840,
                                description="Décalage horaire en minutes pour les dates (ex. 180 pour UTC+3)"),
        filters: dict = Depends(audit_filters),
        db: Session = Depends(database.get_db),
        current_user: int = Depends(Oauth.get_current_user)):
    total = AuditRepository.count(db, **filters)
    if total > EXPORT_LIMIT:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Trop de lignes à exporter ({total}). Affinez les filtres (maximum {EXPORT_LIMIT}).")

    rows = AuditRepository.list_all(db, **filters)
    # BOM UTF-8 : Excel détecte l'encodage et affiche correctement les accents
    content = "\ufeff" + AuditService.to_csv(rows, utc_offset)
    filename = f"audits-{datetime.now(UTC).date().isoformat()}.csv"
    return Response(content=content.encode("utf-8"), media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})