from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.report import CategoryReportItem, MonthReportItem, SummaryResponse


class ReportService:
    def __init__(self, db: Session):
        self.transactions = TransactionRepository(db)

    def summary(self, user: User) -> SummaryResponse:
        income, expense = self.transactions.summary_for_user(user.id)
        return SummaryResponse(
            total_income=income,
            total_expense=expense,
            net=income - expense,
        )

    def by_category(self, user: User) -> list[CategoryReportItem]:
        rows = self.transactions.totals_by_category(user.id)
        items: list[CategoryReportItem] = []
        for category_id, category_name, transaction_type, total in rows:
            items.append(
                CategoryReportItem(
                    category_id=str(category_id) if category_id else None,
                    category_name=category_name or "Uncategorized",
                    transaction_type=int(transaction_type),
                    total=Decimal(str(total or 0)),
                )
            )
        return items

    def by_month(self, user: User) -> list[MonthReportItem]:
        rows = self.transactions.totals_by_month(user.id)
        items: list[MonthReportItem] = []
        for year, month, total_income, total_expense in rows:
            income = Decimal(str(total_income or 0))
            expense = Decimal(str(total_expense or 0))
            items.append(
                MonthReportItem(
                    year=int(year),
                    month=int(month),
                    total_income=income,
                    total_expense=expense,
                    net=income - expense,
                )
            )
        return items
