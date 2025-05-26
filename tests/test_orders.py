import pytest
from fastapi.testclient import TestClient

# A fixture 'client' será automaticamente descoberta do conftest.py

def test_create_product(client: TestClient):
    response = client.post("/products/", json={
        "name": "Produto Teste",
        "description": "Descrição do produto",
        "price": 50.0,
        "stock": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Produto Teste"
    assert data["price"] == 50.0
    # Adicione mais asserções conforme a estrutura do seu ProductOut

def test_get_products(client: TestClient):
    # Opcional: Crie alguns produtos primeiro para garantir que a lista não esteja vazia
    client.post("/products/", json={"name": "Produto A", "description": "Desc A", "price": 10.0, "stock": 1})
    client.post("/products/", json={"name": "Produto B", "description": "Desc B", "price": 20.0, "stock": 2})

    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2 # Pelo menos os produtos que criamos

def test_update_product(client: TestClient):
    # Primeiro cria um produto para atualizar
    create_resp = client.post("/products/", json={
        "name": "Produto Atualizar",
        "description": "Descricao",
        "price": 20.0,
        "stock": 5
    })
    assert create_resp.status_code == 200
    prod_id = create_resp.json()["id"]

    update_resp = client.put(f"/products/{prod_id}", json={
        "name": "Produto Atualizado",
        "price": 30.0
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Produto Atualizado"
    assert update_resp.json()["price"] == 30.0
    # Verifique também se outros campos não alterados permanecem
    assert update_resp.json()["description"] == "Descricao"
    assert update_resp.json()["stock"] == 5

def test_delete_product(client: TestClient):
    # Cria um produto para deletar
    create_resp = client.post("/products/", json={
        "name": "Produto Deletar",
        "description": "Descricao",
        "price": 15.0,
        "stock": 3
    })
    assert create_resp.status_code == 200
    prod_id = create_resp.json()["id"]

    del_resp = client.delete(f"/products/{prod_id}")
    assert del_resp.status_code == 204 # HTTP 204 No Content para deleção bem-sucedida

    # Verifica se produto não existe mais
    get_resp = client.get(f"/products/{prod_id}")
    assert get_resp.status_code == 404
