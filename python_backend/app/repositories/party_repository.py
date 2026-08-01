import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.party import Party


class PartyRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: uuid.UUID) -> list[Party]:
        statement = (
            select(Party)
            .where(or_(Party.is_system.is_(True), Party.user_id == user_id))
            .order_by(Party.is_system.desc(), Party.name)
        )
        return list(self.db.scalars(statement).all())

    def get_accessible(self, party_id: uuid.UUID, user_id: uuid.UUID) -> Party | None:
        statement = select(Party).where(
            Party.id == party_id,
            or_(Party.is_system.is_(True), Party.user_id == user_id),
        )
        return self.db.scalars(statement).first()

    def create_for_user(self, user_id: uuid.UUID, name: str) -> Party:
        party = Party(user_id=user_id, name=name.strip(), is_system=False)
        self.db.add(party)
        self.db.commit()
        self.db.refresh(party)
        return party
