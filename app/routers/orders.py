# routers/orders.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.order import OrderCreate, OrderOut
from services.order_service import create_order, get_orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut)
def create(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return {"message": "Get orders endpoint"}

@router.post("/")
def create_order():
    return {"message": "Create order endpoint"}

@router.get("/{id}")
def get_order(id: int):
    return {"message": f"Get order {id} endpoint"}

@router.put("/{id}")
def update_order(id: int):
    return {"message": f"Update order {id} endpoint"}

@router.delete("/{id}")
def delete_order(id: int):
    return {"message": f"Delete order {id} endpoint"}
