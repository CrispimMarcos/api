from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., description="ID do produto.", example=1)
    quantity: int = Field(..., gt=0, description="Quantidade do produto.", example=2)

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    client_id: int = Field(..., description="ID do cliente que está fazendo o pedido.", example=101)
    items: List[OrderItemCreate] = Field(..., description="Lista de itens no pedido.")

class OrderUpdate(BaseModel):
    client_id: Optional[int] = Field(None, description="Novo ID do cliente, se houver alteração.", example=102)
    status: Optional[str] = Field(None, description="Status do pedido (pending, completed, cancelled).", example="completed", pattern="^(pending|completed|cancelled)$")

class OrderOut(BaseModel):
    id: int
    client_id: int
    total: Decimal
    order_date: datetime
    status: str
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            Decimal: lambda d: float(d),
        }