from decimal import Decimal

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    net: Decimal


class CategoryReportItem(BaseModel):
    category_id: str | None
    category_name: str
    transaction_type: int
    total: Decimal


class MonthReportItem(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    net: Decimal
