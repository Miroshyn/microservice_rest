import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
TOKEN = "Bearer fake-token-for-alice@example.com"

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
        r = await client.post(BASE_URL, json={"productId": 101, "qty": 100},
                              headers={"Authorization": TOKEN})
        assert r.status_code == 400  # Очікується помилка, у коді створюється замовлення
