from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.utils.decorators import monitor_requests_middleware

app = FastAPI()

@app.middleware("http")
async def middleware(request, call_next):
    return await monitor_requests_middleware(request, call_next)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

client = TestClient(app)

def test_middleware():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
