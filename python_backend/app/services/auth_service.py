from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserRead


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, payload: UserCreate) -> TokenResponse:
        existing = self.users.get_by_username(payload.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        user = self.users.create(
            username=payload.username,
            password_hash=hash_password(payload.password),
        )
        return self._token_for(user)

    def login(self, payload: UserLogin) -> TokenResponse:
        user = self.users.get_by_username(payload.username)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        return self._token_for(user)

    def _token_for(self, user: User) -> TokenResponse:
        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token, user=UserRead.model_validate(user))
