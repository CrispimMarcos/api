from sqlalchemy.orm import Session, selectinload
from datetime import datetime, timezone
from app.models.order_model import Order, OrderItem
from app.models.client_model import Client
from app.models.product_model import Product
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderItemCreate
from app.services.whatsapp import send_whatsapp_message
from fastapi import HTTPException
from decimal import Decimal

def create_order(db: Session, order_data: OrderCreate):
    db_order = Order(
        client_id=order_data.client_id,
        order_date=datetime.now(timezone.utc)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    calculated_total = Decimal('0.00')

    for item_data in order_data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto com ID {item_data.product_id} não encontrado.")

        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(db_order_item)

        calculated_total += product.sale_price * item_data.quantity

    db_order.total = calculated_total

    db.commit()
    db.refresh(db_order)

    cliente = db.query(Client).filter(Client.id == db_order.client_id).first()
    if cliente and cliente.phone:
        mensagem = f"Olá {cliente.name}, seu pedido #{db_order.id} foi criado com sucesso! Total: R$ {db_order.total:.2f}"
        try:
            send_whatsapp_message(cliente.phone, mensagem)
        except Exception as e:
            print(f"Erro notificando cliente no WhatsApp: {e}")

    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).options(selectinload(Order.items)).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).options(selectinload(Order.items)).filter(Order.id == order_id).first()

def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        update_data = order_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete(synchronize_session=False)
        db.delete(db_order)
        db.commit()
        return True
    return False