import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.core.constants import TRANSACTION_TYPE_EXPENSE, TRANSACTION_TYPE_INCOME
from app.models.category import Category
from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: uuid.UUID) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id, Transaction.is_deleted.is_(False))
            .order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    def get_for_user(self, transaction_id: uuid.UUID, user_id: uuid.UUID) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
            Transaction.is_deleted.is_(False),
        )
        return self.db.scalars(statement).first()

    def create(
        self,
        *,
        user_id: uuid.UUID,
        transaction_date: datetime,
        transaction_type: int,
        amount: Decimal,
        party_id: uuid.UUID | None,
        category_id: uuid.UUID | None,
        description: str | None,
    ) -> Transaction:
        row = Transaction(
            user_id=user_id,
            transaction_date=transaction_date,
            transaction_type=transaction_type,
            amount=amount,
            party_id=party_id,
            category_id=category_id,
            description=description,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def save(self, row: Transaction) -> Transaction:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Transaction) -> None:
        row.is_deleted = True
        self.db.add(row)
        self.db.commit()

    def summary_for_user(self, user_id: uuid.UUID) -> tuple[Decimal, Decimal]:
        income = self.db.scalar(
            select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
                Transaction.transaction_type == TRANSACTION_TYPE_INCOME,
            )
        )
        expense = self.db.scalar(
            select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
                Transaction.transaction_type == TRANSACTION_TYPE_EXPENSE,
            )
        )
        return Decimal(str(income)), Decimal(str(expense))

    def totals_by_category(self, user_id: uuid.UUID) -> list[tuple]:
        statement = (
            select(
                Category.id,
                Category.name,
                Transaction.transaction_type,
                func.sum(Transaction.amount),
            )
            .select_from(Transaction)
            .outerjoin(Category, Category.id == Transaction.category_id)
            .where(Transaction.user_id == user_id, Transaction.is_deleted.is_(False))
            .group_by(Category.id, Category.name, Transaction.transaction_type)
            .order_by(Transaction.transaction_type, Category.name)
        )
        return list(self.db.execute(statement).all())

    def totals_by_month(self, user_id: uuid.UUID) -> list[tuple]:
        year_col = extract("year", Transaction.transaction_date)
        month_col = extract("month", Transaction.transaction_date)
        statement = (
            select(
                year_col.label("year"),
                month_col.label("month"),
                func.coalesce(
                    func.sum(Transaction.amount).filter(
                        Transaction.transaction_type == TRANSACTION_TYPE_INCOME
                    ),
                    0,
                ).label("total_income"),
                func.coalesce(
                    func.sum(Transaction.amount).filter(
                        Transaction.transaction_type == TRANSACTION_TYPE_EXPENSE
                    ),
                    0,
                ).label("total_expense"),
            )
            .where(Transaction.user_id == user_id, Transaction.is_deleted.is_(False))
            .group_by(year_col, month_col)
            .order_by(year_col.desc(), month_col.desc())
        )
        return list(self.db.execute(statement).all())
