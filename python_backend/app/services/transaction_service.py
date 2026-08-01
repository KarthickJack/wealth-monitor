import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.party_repository import PartyRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate


class TransactionService:
    def __init__(self, db: Session):
        self.transactions = TransactionRepository(db)
        self.categories = CategoryRepository(db)
        self.parties = PartyRepository(db)

    def list_transactions(self, user: User) -> list[TransactionRead]:
        rows = self.transactions.list_for_user(user.id)
        return [TransactionRead.model_validate(row) for row in rows]

    def create_transaction(self, user: User, payload: TransactionCreate) -> TransactionRead:
        self._validate_refs(user.id, payload.category_id, payload.party_id, payload.transaction_type)
        row = self.transactions.create(
            user_id=user.id,
            transaction_date=payload.transaction_date,
            transaction_type=payload.transaction_type,
            amount=payload.amount,
            party_id=payload.party_id,
            category_id=payload.category_id,
            description=payload.description,
        )
        return TransactionRead.model_validate(row)

    def update_transaction(
        self, user: User, transaction_id: uuid.UUID, payload: TransactionUpdate
    ) -> TransactionRead:
        row = self._get_owned(user.id, transaction_id)
        data = payload.model_dump(exclude_unset=True)

        next_type = data.get("transaction_type", row.transaction_type)
        next_category = data.get("category_id", row.category_id)
        next_party = data.get("party_id", row.party_id)
        self._validate_refs(user.id, next_category, next_party, next_type)

        for key, value in data.items():
            setattr(row, key, value)

        saved = self.transactions.save(row)
        return TransactionRead.model_validate(saved)

    def delete_transaction(self, user: User, transaction_id: uuid.UUID) -> None:
        row = self._get_owned(user.id, transaction_id)
        self.transactions.soft_delete(row)

    def _get_owned(self, user_id: uuid.UUID, transaction_id: uuid.UUID) -> Transaction:
        row = self.transactions.get_for_user(transaction_id, user_id)
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return row

    def _validate_refs(
        self,
        user_id: uuid.UUID,
        category_id: uuid.UUID | None,
        party_id: uuid.UUID | None,
        transaction_type: int,
    ) -> None:
        if category_id is not None:
            category = self.categories.get_accessible(category_id, user_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid category",
                )
            if category.transaction_type != transaction_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category does not match transaction type",
                )

        if party_id is not None:
            party = self.parties.get_accessible(party_id, user_id)
            if not party:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid party",
                )
