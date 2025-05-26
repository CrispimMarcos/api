from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order_schema import OrderCreate, OrderOut, OrderUpdate
from app.services.order_service import (
    create_order,
    get_orders,
    get_order_by_id,
    update_order as service_update_order,
    delete_order as service_delete_order,
)

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.get("/", response_model=list[OrderOut])
def list_all_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/{order_id}", response_model=OrderOut)
def get_single_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    return db_order

@router.put("/{order_id}", response_model=OrderOut)
def update_existing_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db)
):
    db_order = service_update_order(db, order_id, order)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado para atualização")
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    success = service_delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado para exclusão")
    return