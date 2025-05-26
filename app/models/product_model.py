from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Numeric
from app.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    sale_price = Column(Numeric(precision=10, scale=2), nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    section = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=True)
    available = Column(Boolean, default=True)
    order_items = relationship("OrderItem", back_populates="product")

