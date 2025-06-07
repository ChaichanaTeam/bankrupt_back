import pytest
from requests import Session
from conftest import client
from constants import *
from src.core.traceback import traceBack

def test_login(client: Session):
    cookie = client.cookies.get("authorization")
    r = client.get(f"{BASE_URL}/auth/me", cookies={"authorization": cookie})

    assert r.status_code == 200, f"Me get failed: {r.text}"
    
    data = r.json()
    
    assert "name" in data
    
    print()
    traceBack("Login success:", data)

    r = client.post(f"{BASE_URL}/auth/logout")
    assert r.cookies.get("authorization") == None, f"Logout failed"

    traceBack("Logout success")