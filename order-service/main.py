import os
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="OrderService")

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8001")
PRODUCT_URL = os.getenv("PRODUCT_URL", "http://product-service:8002")

ORDERS: list[dict] = []

@app.post("/orders")
async def create_order(payload: dict, authorization: str | None = Header(default=None)):
    product_id = payload.get("productId")
    qty = payload.get("qty")

    # Перевірка токена
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{AUTH_URL}/whoami", headers={"Authorization": authorization or ""})
        if r.status_code != 200:
            return JSONResponse({"error": "unauthorized"}, status_code=401)

    # Перевірка наявності товару
    async with httpx.AsyncClient() as client:
        prod = await client.get(f"{PRODUCT_URL}/products/{product_id}")
        if prod.status_code != 200:
            return JSONResponse({"error": "product not found"}, status_code=404)
        if prod.json()["inStock"] < qty:
            return JSONResponse({"error": "insufficient stock"}, status_code=400)

    # Створення замовлення
    order = {
        "order_id": len(ORDERS) + 1,
        "product_id": product_id,
        "quantity": qty,
        "status": "created",
    }
    ORDERS.append(order)
    return JSONResponse(order, status_code=201)

@app.get("/orders")
async def list_orders():
    return {"orders": ORDERS}
