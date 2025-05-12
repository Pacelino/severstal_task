import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app 
from tests.confile import create_table

@pytest.mark.parametrize(
    "params, status_code, expected_error_message", 
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "length"
                    ],
                    "msg": "Field required",
                    "input": {}
                    },
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "weight"
                    ],
                    "msg": "Field required",
                    "input": {}
                    }
                ]
            }
        ),
        (
            {"length": -1,"weight": 1},
            422,
            {
                "detail": [
                    {
                    "type": "greater_than",
                    "loc": [
                        "body",
                        "length"
                    ],
                    "msg": "Input should be greater than 0",
                    "input": -1,
                    "ctx": {
                        "gt": 0
                    }
                    }
                ]
            }
        ),
    ]
)
def test_negative_create_rolls(params, status_code, expected_error_message):
    client = TestClient(app)
    response = client.post("/api/add_rolls/", json=params)
    
    assert response.status_code == status_code
    assert response.json() == expected_error_message



def test_create_rolls(create_table):

    app.dependency_overrides[get_session] = create_table()
    client = TestClient(app)
    response = client.post("/api/add_rolls/", json={"length": 228,"weight": 228})
    
    app.dependency_overrides.clear()
    data = response.json()
    
    assert response.status_code == 200
    assert data["length"] == 228
    assert data["weight"] == 228