from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import Token, UserCreate, UserOut
from app.auth.auth_service import authenticate_user, get_password_hash
from app.auth.jwt_handler import create_access_token, decode_access_token
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token,
             summary="Autenticar usuário",
             description="Use seu username (ou email) e senha para obter um token JWT. Este endpoint é usado pelo botão 'Authorize' no Swagger UI.")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas: username ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user.email, "role": user.role, "username": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut,
             summary="Registrar novo usuário")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user_by_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado.")
    
    existing_user_by_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado.")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role if user_data.role else "user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/refresh-token", response_model=Token,
             summary="Atualizar token de acesso")
def refresh_token(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado", headers={"WWW-Authenticate": "Bearer"})
    
    username = payload.get("username")
    email = payload.get("sub")
    role = payload.get("role", "user")

    if not username: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload inválido: username ausente.", headers={"WWW-Authenticate": "Bearer"})
    new_token = create_access_token(data={"sub": username, "role": role, "email": email})

    return {"access_token": new_token, "token_type": "bearer"}