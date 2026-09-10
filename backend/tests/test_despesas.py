def test_criar_despesa(client):
    response = client.post(
        "/despesas",
        json={
            "ano": 2026,
            "mes": 9,
            "dia": 10,
            "tipo": "DevOps",
            "descricao": "Teste automatizado",
            "valor": 150.50
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ano"] == 2026
    assert data["mes"] == 9
    assert data["dia"] == 10
    assert data["tipo"] == "DevOps"
    assert data["descricao"] == "Teste automatizado"
    assert data["valor"] == "150.50"
    assert "id" in data


def test_listar_despesas(client):
    client.post(
        "/despesas",
        json={
            "ano": 2026,
            "mes": 9,
            "dia": 10,
            "tipo": "Alimentação",
            "descricao": "Almoço",
            "valor": 35.90
        }
    )

    response = client.get("/despesas")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["descricao"] == "Almoço"


def test_remover_despesa(client):
    create_response = client.post(
        "/despesas",
        json={
            "ano": 2026,
            "mes": 9,
            "dia": 10,
            "tipo": "Transporte",
            "descricao": "Uber",
            "valor": 25.00
        }
    )

    despesa_id = create_response.json()["id"]

    response = client.delete(f"/despesas/{despesa_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == despesa_id
    assert data["message"] == "Despesa removida com sucesso"
