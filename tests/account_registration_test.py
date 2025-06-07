import pytest
from requests import Session
from conftest import client
from constants import *
from src.core.traceback import traceBack

def test_create_card(client: Session):
    cookie = client.cookies.get("authorization")
    r = client.post(f"{BASE_URL}/card/create", cookies={"authorization": cookie})

    assert r.status_code == 200, f"Card creation failed: {r.text}"
    
    data = r.json()
    
    assert "number" in data or "card_number" in data
    
    traceBack("Card created:", data)

    client.post(f"{BASE_URL}/auth/logout")