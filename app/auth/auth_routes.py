# app/auth/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin, Token
from app.auth.auth_service import authenticate_user
from app.auth.jwt_handler import create_access_token
from app.schemas import UserCreate, UserOut
from app.auth.auth_service import get_password_hash
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import create_access_token, decode_access_token
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        role="user" ,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/refresh-token", response_model=Token)
def refresh_token(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    email = payload.get("sub")
    role = payload.get("role", "user")
    new_token = create_access_token(data={"sub": email, "role": role})
    return {"access_token": new_token, "token_type": "bearer"}
