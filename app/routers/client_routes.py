from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientOut
from app.services.clients import (
    create_client,
    get_clients,
    get_client_by_id,
    update_client,
    delete_client
)

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientOut)
def create(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.get("/", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return get_clients(db)

@router.get("/{client_id}", response_model=ClientOut)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.put("/{client_id}", response_model=ClientOut)
def update(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    return update_client(db, client_id, payload)

@router.delete("/{client_id}")
def delete(client_id: int, db: Session = Depends(get_db)):
    delete_client(db, client_id)
    return {"message": "Cliente deletado com sucesso"}
