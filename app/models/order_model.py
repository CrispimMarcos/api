from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status = Column(String, default="pending", index=True)
    order_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    total = Column(Numeric(precision=10, scale=2), nullable=True, default=0.0)

    client = relationship("Client", back_populates="orders")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")