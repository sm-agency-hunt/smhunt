from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from src.core.security import (
    verify_password, create_access_token,
    get_current_user
)
from src.core.config import settings
from src.database.connection import get_db_session
from src.database.models import User

from datetime import timedelta
from src.core.logger import log

router = APIRouter()
security = HTTPBearer()

# Pydantic models


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Authentication endpoints


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Authenticate user and return access token"""
    try:
        with get_db_session() as db:
            user = (
                db.query(User)
                .filter(User.email == credentials.email)
                .first()
            )

            if not user or not verify_password(
                credentials.password,
                user.hashed_password
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is disabled"
                )

            # Create access token
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = create_access_token(
                data={"sub": user.email, "user_id": user.id},
                expires_delta=access_token_expires
            )

            user_response = UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser
            )

            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=user_response
            )

    except Exception as e:
        log.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """Get current authenticated user information"""
    try:
        with get_db_session() as db:
            user_id = current_user.get("user_id")
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            return UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser
            )

    except Exception as e:
        log.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )
