import pytest
import httpx

BASE_URL = "http://localhost:8003/orders"
AUTH_URL = "http://localhost:8001"
PRODUCT_URL = "http://localhost:8002"

USER = {"email": "alice@example.com", "password": "alicepwd"}
PRODUCT_ID = 101
INSUFFICIENT_QTY = 100

@pytest.mark.asyncio
async def test_create_order_insufficient_stock():
    async with httpx.AsyncClient() as client:
        reg_resp = await client.post(f"{AUTH_URL}/register", json=USER)
        assert reg_resp.status_code in (200, 201), f"Register failed: {reg_resp.text}"

        login_resp = await client.post(f"{AUTH_URL}/login", json=USER)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["access_token"]


        prod_resp = await client.get(f"{PRODUCT_URL}/products/{PRODUCT_ID}")
        assert prod_resp.status_code == 200, f"Product not found: {prod_resp.text}"
        stock = prod_resp.json()["inStock"]
        assert stock < INSUFFICIENT_QTY, "Stock too high for this test"

        order_resp = await client.post(
            BASE_URL,
            json={"productId": PRODUCT_ID, "qty": INSUFFICIENT_QTY},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert order_resp.status_code == 400, f"Expected 400, got {order_resp.status_code}"
