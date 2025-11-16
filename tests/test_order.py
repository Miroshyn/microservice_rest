import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"

TOKEN = "Bearer fake-token-for-alice@example.com"

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    async with httpx.AsyncClient() as client:
        # Логін через GET
        login_resp = await client.get(f"{AUTH_URL}/login", params={
            "email": "alice@example.com",
            "password": "alice123"
        })
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["accessToken"]

        # Створення замовлення з кількістю більше за наявну
        r = await client.post(
            BASE_URL,
            json={"productId": 101, "qty": 100},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert r.status_code == 400
