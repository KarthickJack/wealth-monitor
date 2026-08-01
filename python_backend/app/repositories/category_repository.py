import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: uuid.UUID) -> list[Category]:
        statement = (
            select(Category)
            .where(or_(Category.is_system.is_(True), Category.user_id == user_id))
            .order_by(Category.is_system.desc(), Category.name)
        )
        return list(self.db.scalars(statement).all())

    def get_accessible(self, category_id: uuid.UUID, user_id: uuid.UUID) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id,
            or_(Category.is_system.is_(True), Category.user_id == user_id),
        )
        return self.db.scalars(statement).first()

    def create_for_user(
        self, user_id: uuid.UUID, name: str, transaction_type: int
    ) -> Category:
        category = Category(
            user_id=user_id,
            name=name.strip(),
            transaction_type=transaction_type,
            is_system=False,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
