from fastapi.testclient import TestClient
from main import app, MIN_AMOUNT, MAX_AMOUNT

client = TestClient(app)

def test_user_with_debt():
    response = client.post("/api/decision", json={
        "loan_amount": 4000,
        "loan_period": 12,
        "personal_code": "49002010965"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["approved"] == False
    assert'debt' in data["message"].lower()


def test_user_finding_new_period():
    response = client.post(
        "/api/decision",
        json={"personal_code": "49002010976",
              "loan_amount": 4000, "loan_period": 12}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["approved"] is True
    assert data["amount"] == MIN_AMOUNT  
    assert data["period"] == 20


def test_user_standard_approval():
    response = client.post(
        "/api/decision",
        json={"personal_code": "49002010987",
              "loan_amount": 4000, "loan_period": 12}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["approved"] is True
    assert data["amount"] == 3600
    assert data["period"] == 12


def test_user_max_limit_cap():
    response = client.post(
        "/api/decision",
        json={"personal_code": "49002010998",
              "loan_amount": 4000, "loan_period": 12}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["approved"] is True
    assert data["amount"] == MAX_AMOUNT 
    assert data["period"] == 12


def test_invalid_personal_code():
    response = client.post(
        "/api/decision",
        json={"personal_code": "00000000000",
              "loan_amount": 4000, "loan_period": 12}
    )
    assert response.status_code == 404


def test_validation_error_amount_too_low():
    response = client.post(
        "/api/decision",
        json={"personal_code": "49002010987", "loan_amount": 1000,
              "loan_period": 12} 
    )
    assert response.status_code == 422  
