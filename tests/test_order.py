import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_create_order_invalid_token():
    """Помилка: створення замовлення без перевірки токена"""
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 1},
                              headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    """Помилка: створення замовлення без перевірки наявності товару"""
    async with httpx.AsyncClient() as client:
        # Отримати валідний токен від auth-service
        login_resp = await client.post(f"{AUTH_URL}/login", json={"email": "alice@example.com", "password": "alicepwd"})
        token = login_resp.json()["access_token"]

        # Надіслати запит з qty > inStock
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 100},
                              headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 400
