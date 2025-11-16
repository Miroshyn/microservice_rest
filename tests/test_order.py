import pytest
import httpx
import os

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"  # URL вашого auth-service

@pytest.mark.asyncio
async def test_create_order_invalid_token():
    """Створення замовлення з неправильним токеном повертає 401"""
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 1},
                              headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    """Створення замовлення з кількістю більшу за наявну повертає 400"""
    async with httpx.AsyncClient() as client:
        # Отримати валідний токен від auth-service
        login_resp = await client.get(f"{AUTH_URL}/login", params={
            "email": "alice@example.com",
            "password": "alicepwd"
        })
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["access_token"]

        # Спроба створити замовлення з кількістю більше, ніж на складі
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 100},
                              headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 400
