import pytest
import httpx

BASE_URL = "http://localhost:8002"

@pytest.mark.asyncio
async def test_get_nonexistent_product():
    """Помилка: /products/{pid} повертає 200 замість 404"""
    async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL + "/products/9999")
        assert r.status_code == 404

@pytest.mark.asyncio
async def test_product_price_type():
    """Помилка: price зберігається як рядок"""
    async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL + "/products/100")
        data = r.json()
        assert isinstance(data["price"], float)  # У початковому коді str
