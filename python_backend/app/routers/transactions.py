import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
def list_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TransactionService(db).list_transactions(current_user)


@router.post("", response_model=TransactionRead, status_code=201)
def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TransactionService(db).create_transaction(current_user, payload)


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: uuid.UUID,
    payload: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TransactionService(db).update_transaction(current_user, transaction_id, payload)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    TransactionService(db).delete_transaction(current_user, transaction_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
