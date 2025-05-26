from fastapi import APIRouter
from . import auth_routes, client_routes, order_routes, product_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router)
api_router.include_router(order_routes.router)
api_router.include_router(client_routes.router)
api_router.include_router(product_routes.router)
