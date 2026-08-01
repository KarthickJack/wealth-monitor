from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CategoryService(db).list_categories(current_user)


@router.post("", response_model=CategoryRead, status_code=201)
def create_category(
    payload: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CategoryService(db).create_category(current_user, payload)
