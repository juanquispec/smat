from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def obtener_token_prueba():
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    return response.json()["access_token"]

def test_crear_estacion():
    token = obtener_token_prueba()
    response = client.post("/estaciones/", json={
        "id": 1,
        "nombre": "Estación Rimac",
        "ubicacion": "Chosica"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [201, 400] 

def test_registrar_lectura():
    token = obtener_token_prueba()
    response = client.post("/lecturas/", json={
        "estacion_id": 1,
        "valor": 12.5
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

def test_historial_y_promedio():
    token = obtener_token_prueba()
    client.post("/estaciones/", json={"id": 20, "nombre": "Rio Yauli", "ubicacion": "La Oroya"}, headers={"Authorization": f"Bearer {token}"})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 10.0}, headers={"Authorization": f"Bearer {token}"})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 20.0}, headers={"Authorization": f"Bearer {token}"})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 30.0}, headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/estaciones/20/historial")
    assert response.status_code == 200
    data = response.json()
    assert data["estacion_id"] == 20
    assert data["promedio"] == 20.0