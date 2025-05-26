def test_create_product(client):
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

def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product(client):
    # Primeiro cria um produto para atualizar
    create_resp = client.post("/products/", json={
        "name": "Produto Atualizar",
        "description": "Descricao",
        "price": 20.0,
        "stock": 5
    })
    prod_id = create_resp.json()["id"]

    update_resp = client.put(f"/products/{prod_id}", json={
        "name": "Produto Atualizado",
        "price": 30.0
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Produto Atualizado"
    assert update_resp.json()["price"] == 30.0

def test_delete_product(client):
    # Cria um produto para deletar
    create_resp = client.post("/products/", json={
        "name": "Produto Deletar",
        "description": "Descricao",
        "price": 15.0,
        "stock": 3
    })
    prod_id = create_resp.json()["id"]

    del_resp = client.delete(f"/products/{prod_id}")
    assert del_resp.status_code == 204

    # Verifica se produto não existe mais
    get_resp = client.get(f"/products/{prod_id}")
    assert get_resp.status_code == 404
