import pytest
import httpx

BASE_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Помилка: /login повертає 200 замість 401"""
    async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL + "/login", params={"email": "alice@example.com", "password": "wrong"})
        assert r.status_code == 401  # У початковому коді значення дорівнює 200

@pytest.mark.asyncio
async def test_whoami_no_token():
    """Помилка: /whoami повертає 200 замість 401 при відсутньому токені"""
    async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL + "/whoami")
        assert r.status_code == 401
