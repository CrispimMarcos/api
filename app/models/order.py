from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client")
    products = relationship("Product", secondary=order_products)
