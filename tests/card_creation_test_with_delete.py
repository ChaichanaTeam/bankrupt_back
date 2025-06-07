import pytest
from requests import Session
from conftest import client, card_balance_set
from constants import *
from src.core.traceback import traceBack

def test_create_card(client: Session):
    print()

    cookie = client.cookies.get("authorization")
    r = client.post(f"{BASE_URL}/card/create", cookies={"authorization": cookie})

    assert r.status_code == 200, f"Card creation failed: {r.text}"
    
    data = r.json()
    
    assert "number" in data
    
    traceBack("Card created:", data)
    card_number = data["number"]

    card_balance_set(0, card_number)
    r = client.get(f"{BASE_URL}/card/{card_number[-4:]}", cookies={"authorization": cookie})

    data = r.json()

    assert "number" in data, f"Card getting failed: {r.text}"
    traceBack("Balance changed to 0:", data["balance"], "of ", card_number)

    r = client.delete(f"{BASE_URL}/card/delete", json={"card_number": card_number}, cookies={"authorization": cookie})
    assert r.status_code == 200, f"Card delete failed: {r.text}"

    traceBack(f"Card with number {card_number} deleted")

    client.post(f"{BASE_URL}/auth/logout")
    assert r.cookies.get("authorization") == None, f"Logout failed"

    traceBack("Logout success")