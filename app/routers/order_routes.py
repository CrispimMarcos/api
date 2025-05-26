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
import sentry_sdk

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order(db, order)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Erro ao criar o pedido.")

@router.get("/", response_model=list[OrderOut])
def list_all_orders(db: Session = Depends(get_db)):
    try:
        return get_orders(db)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos.")

@router.get("/{order_id}", response_model=OrderOut)
def get_single_order(order_id: int, db: Session = Depends(get_db)):
    try:
        db_order = get_order_by_id(db, order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return db_order
    except HTTPException as e:
        sentry_sdk.capture_exception(e)
        raise e
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Erro ao buscar o pedido.")

@router.put("/{order_id}", response_model=OrderOut)
def update_existing_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    try:
        db_order = service_update_order(db, order_id, order)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado para atualização")
        return db_order
    except HTTPException as e:
        sentry_sdk.capture_exception(e)
        raise e
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Erro ao atualizar o pedido.")

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    try:
        success = service_delete_order(db, order_id)
        if not success:
            raise HTTPException(status_code=404, detail="Pedido não encontrado para exclusão")
        return
    except HTTPException as e:
        sentry_sdk.capture_exception(e)
        raise e
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Erro ao excluir o pedido.")
