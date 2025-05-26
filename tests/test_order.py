import pytest
from fastapi.testclient import TestClient 
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.models.client_model import Client

# Dados de teste para criar cliente e produto
CLIENT_DATA = {
    "name": "Cliente Teste",
    "email": "cliente@teste.com",
    "phone": "11987654321"
}

PRODUCT_1_DATA = {
    "name": "Fone de Ouvido",
    "description": "Fone de ouvido Bluetooth",
    "price": 100.00,
    "sale_price": 90.00,
    "stock": 50
}

PRODUCT_2_DATA = {
    "name": "Mouse Gamer",
    "description": "Mouse ergonômico para jogos",
    "price": 150.00,
    "sale_price": 130.00,
    "stock": 30
}

@pytest.fixture
def setup_order_data(client: Client, db_session: Session):
    # Cria um cliente
    client_response = client.post("/clients/", json=CLIENT_DATA)
    assert client_response.status_code == 200
    test_client = client_response.json()

    # Cria produtos
    product1_response = client.post("/products/", json=PRODUCT_1_DATA)
    assert product1_response.status_code == 200
    test_product1 = product1_response.json()

    product2_response = client.post("/products/", json=PRODUCT_2_DATA)
    assert product2_response.status_code == 200
    test_product2 = product2_response.json()

    return {
        "client": test_client,
        "product1": test_product1,
        "product2": test_product2
    }

def test_create_order(client: Client, setup_order_data: dict, mocker):
    # Mock send_whatsapp_message para não tentar enviar SMS real
    mocker.patch("app.services.whatsapp.send_whatsapp_message")

    client_id = setup_order_data["client"]["id"]
    product1_id = setup_order_data["product1"]["id"]
    product2_id = setup_order_data["product2"]["id"]
    
    order_data = {
        "client_id": client_id,
        "items": [
            {"product_id": product1_id, "quantity": 2},
            {"product_id": product2_id, "quantity": 1}
        ]
    }

    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["client_id"] == client_id
    assert data["status"] == "pending"
    assert "order_date" in data
    assert data["total"] == (PRODUCT_1_DATA["sale_price"] * 2) + (PRODUCT_2_DATA["sale_price"] * 1)
    assert len(data["items"]) == 2
    assert mocker.patch.called # Verifica se a função mockada foi chamada

def test_create_order_product_not_found(client: Client, setup_order_data: dict, mocker):
    mocker.patch("app.services.whatsapp.send_whatsapp_message")
    client_id = setup_order_data["client"]["id"]

    order_data = {
        "client_id": client_id,
        "items": [
            {"product_id": 99999, "quantity": 1} # ID de produto inexistente
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
    assert "Produto com ID 99999 não encontrado" in response.json()["detail"]

@pytest.fixture
def create_test_order(client: Client, setup_order_data: dict, mocker):
    # Cria um pedido de teste para outras operações
    mocker.patch("app.services.whatsapp.send_whatsapp_message") # Mock novamente
    client_id = setup_order_data["client"]["id"]
    product1_id = setup_order_data["product1"]["id"]

    order_data = {
        "client_id": client_id,
        "items": [{"product_id": product1_id, "quantity": 3}]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    return response.json()

def test_list_orders(client: Client, create_test_order: dict):
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verifica se o pedido criado está na lista
    assert any(order["id"] == create_test_order["id"] for order in data)

def test_get_order_by_id(client: Client, create_test_order: dict):
    order_id = create_test_order["id"]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert len(data["items"]) == 1

def test_get_order_not_found(client: Client):
    response = client.get("/orders/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"

def test_update_order_status(client: Client, create_test_order: dict):
    order_id = create_test_order["id"]
    update_data = {"status": "completed"}
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "completed"
    assert data["total"] == create_test_order["total"] # Total não deve mudar na atualização de status

def test_update_order_client_id(client: Client, create_test_order: dict, setup_order_data: dict):
    order_id = create_test_order["id"]
    new_client_id = setup_order_data["client"]["id"] # Reutiliza o cliente existente
    update_data = {"client_id": new_client_id}
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["client_id"] == new_client_id

def test_update_order_not_found(client: Client):
    update_data = {"status": "cancelled"}
    response = client.put("/orders/99999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado para atualização"

def test_delete_order(client: Client, create_test_order: dict):
    order_id = create_test_order["id"]
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204 # No Content
    
    # Tenta buscar o pedido para confirmar a deleção
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404
    

def test_delete_order_not_found(client: Client):
    response = client.delete("/orders/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado para exclusão"