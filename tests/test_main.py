from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_crear_libro():
    nuevo = {"titulo": "El Principito", "autor": "Saint-Exupéry", "isbn": "9781234567890"}
    res = client.post("/libros", json=nuevo)
    assert res.status_code == 201
    assert res.json()["titulo"] == "El Principito"
