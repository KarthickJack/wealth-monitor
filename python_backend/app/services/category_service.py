from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryRead


class CategoryService:
    def __init__(self, db: Session):
        self.categories = CategoryRepository(db)

    def list_categories(self, user: User) -> list[CategoryRead]:
        rows = self.categories.list_for_user(user.id)
        return [CategoryRead.model_validate(row) for row in rows]

    def create_category(self, user: User, payload: CategoryCreate) -> CategoryRead:
        try:
            category = self.categories.create_for_user(
                user_id=user.id,
                name=payload.name,
                transaction_type=payload.transaction_type,
            )
        except IntegrityError as exc:
            self.categories.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists for this type",
            ) from exc
        return CategoryRead.model_validate(category)
