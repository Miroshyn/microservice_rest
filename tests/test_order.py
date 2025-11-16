import pytest
import httpx
import os

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_create_order_invalid_token():
    """Створення замовлення з недійсним токеном повинно повертати 401"""
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 1},
                              headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401


@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    """Створення замовлення з кількістю більшу за наявну повинно повертати 400"""
    async with httpx.AsyncClient() as client:
        # Отримати валідний токен від auth-service
        login_resp = await client.post(f"{AUTH_URL}/login",
                                       json={"email": "alice@example.com", "password": "alicepwd"})
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token_data = login_resp.json()

        # Тут використовуємо правильне поле для токена (можливо "access_token" або "token")
        token = token_data.get("access_token") or token_data.get("token")
        assert token, f"No token in login response: {token_data}"

        headers = {"Authorization": f"Bearer {token}"}

        # Робимо запит на створення замовлення з великою кількістю
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 100}, headers=headers)
        assert r.status_code == 400
