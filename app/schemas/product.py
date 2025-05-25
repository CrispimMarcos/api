from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    description: str
    sale_price: int
    barcode: str
    section: str
    expiration_date: Optional[date] = None
    available: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    description: Optional[str] = None
    sale_price: Optional[int] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiration_date: Optional[date] = None
    available: Optional[int] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
