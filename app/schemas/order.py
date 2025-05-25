from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    client_id: int
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: int
    client_id: int
    total: Decimal
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
