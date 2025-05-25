# app/services/clients.py
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def create_client(db: Session, client_data: ClientCreate):
    new_client = Client(**client_data.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

def get_clients(db: Session):
    return db.query(Client).all()

def get_client_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def update_client(db: Session, client_id: int, data: ClientUpdate):
    client = get_client_by_id(db, client_id)
    if not client:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    client = get_client_by_id(db, client_id)
    if client:
        db.delete(client)
        db.commit()
