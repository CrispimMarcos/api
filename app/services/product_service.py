from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.models.order_model import OrderItem
def create_product(db: Session, product_data: ProductCreate):
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    count = db.query(OrderItem).filter(OrderItem.product_id == product_id).count()
    if count > 0:
        return False
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
        return True
    return False
