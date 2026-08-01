from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.party_repository import PartyRepository
from app.schemas.party import PartyCreate, PartyRead


class PartyService:
    def __init__(self, db: Session):
        self.parties = PartyRepository(db)

    def list_parties(self, user: User) -> list[PartyRead]:
        rows = self.parties.list_for_user(user.id)
        return [PartyRead.model_validate(row) for row in rows]

    def create_party(self, user: User, payload: PartyCreate) -> PartyRead:
        try:
            party = self.parties.create_for_user(user_id=user.id, name=payload.name)
        except IntegrityError as exc:
            self.parties.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Party already exists",
            ) from exc
        return PartyRead.model_validate(party)
