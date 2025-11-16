import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
TOKEN = "Bearer fake-token-for-alice@example.com"  # Фіксований токен для тестів

@pytest.mark.asyncio
async def test_create_order_invalid_token():
    """Створення замовлення з неправильним токеном повертає 401"""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            BASE_URL,
            json={"productId": 101, "qty": 1},
            headers={"Authorization": "Bearer invalid"}
        )
        assert r.status_code == 401

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    """Створення замовлення з кількістю більшу за наявну повертає 400"""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            BASE_URL,
            json={"productId": 101, "qty": 100},  # Кількість більша за наявну
            headers={"Authorization": TOKEN}
        )
        assert r.status_code == 400
