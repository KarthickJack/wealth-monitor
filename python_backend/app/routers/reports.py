from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import CategoryReportItem, MonthReportItem, SummaryResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary", response_model=SummaryResponse)
def summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReportService(db).summary(current_user)


@router.get("/by-category", response_model=list[CategoryReportItem])
def by_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReportService(db).by_category(current_user)


@router.get("/by-month", response_model=list[MonthReportItem])
def by_month(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ReportService(db).by_month(current_user)
