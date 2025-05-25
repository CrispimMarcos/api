# routers/__init__.py
from fastapi import APIRouter
from . import auth, users, clients, products, orders

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(clients.router)
api_router.include_router(products.router)
api_router.include_router(orders.router)
