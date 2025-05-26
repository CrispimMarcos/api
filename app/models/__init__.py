# models/__init__.py
from app.database import Base
from .user_model import User
from .client_model import Client
from .product_model import Product
from .order_model import Order, OrderItem
