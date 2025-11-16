from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="ProductService")

# Pydantic-схема для продукту
class Product(BaseModel):
    product_id: int
    name: str
    price: float
    inStock: int

# Простий каталог товарів
PRODUCTS = [
    {"product_id": 100, "name": "Keyboard", "price": 59.99, "inStock": 5},
    {"product_id": 101, "name": "Mouse", "price": 29.99, "inStock": 0},
]

@app.get("/products")
async def list_products():
    # Конвертуємо price у float на всяк випадок
    items = [{**p, "price": float(p["price"])} for p in PRODUCTS]
    return {"items": items}

@app.get("/products/{pid}", response_model=Product)
async def get_product(pid: int):
    for p in PRODUCTS:
        if p["product_id"] == pid:
            p["price"] = float(p["price"])  # Перетворюємо рядок у float
            return p
    return JSONResponse({"message": "not found"}, status_code=404)  # Замість 200
