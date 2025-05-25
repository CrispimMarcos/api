# routers/products.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut
from app.services.products import create_product, get_products

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductOut)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)


from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_products():
    return {"message": "Get products endpoint"}

@router.post("/")
def create_product():
    return {"message": "Create product endpoint"}

@router.get("/{id}")
def get_product(id: int):
    return {"message": f"Get product {id} endpoint"}

@router.put("/{id}")
def update_product(id: int):
    return {"message": f"Update product {id} endpoint"}

@router.delete("/{id}")
def delete_product(id: int):
    return {"message": f"Delete product {id} endpoint"}
