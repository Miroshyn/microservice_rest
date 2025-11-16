import pytest
import httpx

BASE_URL = "http://order-service:8003/orders"
AUTH_URL = "http://auth-service:8001"

USER = {"email": "alice@example.com", "password": "alice123"}

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    async with httpx.AsyncClient() as client:
        # Отримати токен
        login_resp = await client.get(f"{AUTH_URL}/login", params=USER)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["accessToken"]

        # Створення замовлення з qty > inStock
        r = await client.post(
            BASE_URL,
            json={"productId": 101, "qty": 100},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert r.status_code == 400
