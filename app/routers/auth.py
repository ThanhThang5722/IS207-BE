from fastapi import APIRouter, Depends, HTTPException
from app.schemas.account_schema import LoginRequest, TokenResponse, RegisterRequest
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới (customer hoặc partner)"""
    # TODO: check duplicate username, hash password, insert record
    pass

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Đăng nhập bằng username + password"""
    pass

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    """Lấy access token mới từ refresh token"""
    pass

@router.post("/revoke")
def revoke_token(token: str):
    """Hủy hiệu lực token hiện tại"""
    pass
