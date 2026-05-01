"""Auth service routers — register, login, token management."""
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from common.database import get_db
from common.security import get_security
from common.models import User
from common.repositories import UserRepository
from common.schemas import UserCreate, UserResponse, Token, LoginRequest
from common.exceptions import ConflictException, UnauthorizedException
from common.dependencies import get_current_user, get_admin_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(req: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    repo = UserRepository(db)
    security = get_security()

    existing = repo.get_by_email(req.email)
    if existing:
        raise ConflictException(f"Email '{req.email}' already registered")

    hashed = security.hash_password(req.password)
    user = repo.create(
        email=req.email,
        hashed_password=hashed,
        full_name=req.full_name,
        role=req.role,
    )
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate and return JWT token.

    Accepts form-encoded data (username+password) for OAuth2 compatibility,
    or JSON body with email+password.
    """
    repo = UserRepository(db)
    security = get_security()

    # Accept both form-encoded (username) and JSON (email)
    email = form_data.username

    user = repo.get_by_email(email)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedException("Account is deactivated")

    token = security.create_access_token({
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
    })
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    """List all users (admin only)."""
    repo = UserRepository(db)
    return repo.list()

