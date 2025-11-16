import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"  # URL auth-service

USER = {"email": "alice@example.com", "password": "alicepwd"}

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
        # 1. Реєстрація користувача (щоб login спрацював)
        await client.post(f"{AUTH_URL}/register", json=USER)

        # 2. Отримати валідний токен
        login_resp = await client.post(f"{AUTH_URL}/login", json=USER)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["access_token"]

        # 3. Спроба створити замовлення з qty > inStock
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 100},
                              headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 400  # Очікувана помилка "insufficient stock"
