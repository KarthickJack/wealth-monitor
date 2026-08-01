from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.party import PartyCreate, PartyRead
from app.services.party_service import PartyService

router = APIRouter(prefix="/parties", tags=["parties"])


@router.get("", response_model=list[PartyRead])
def list_parties(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return PartyService(db).list_parties(current_user)


@router.post("", response_model=PartyRead, status_code=201)
def create_party(
    payload: PartyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return PartyService(db).create_party(current_user, payload)
