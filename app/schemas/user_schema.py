from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserLogin(UserBase):
    username: str
    password: str

class UserCreate(UserBase):
    password: str
    email: EmailStr
    username: str
    role: str = "user"
    
class UserOut(UserBase):
    id: int
    email: str
    username: str 
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
