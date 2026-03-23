from fastapi import FastAPI, Query, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ----------------------
# DATA
# ----------------------
menu = [
    {"id": 1, "name": "Pizza", "price": 200, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Burger", "price": 150, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Pasta", "price": 180, "category": "Pizza", "is_available": False},
    {"id": 4, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 5, "name": "Ice Cream", "price": 100, "category": "Dessert", "is_available": True},
    {"id": 6, "name": "Fries", "price": 120, "category": "Burger", "is_available": True},
]

orders = []
order_counter = 1
cart = []

# ----------------------
# DAY 1
# ----------------------
@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}

@app.get("/menu")
def get_menu():
    return {"total": len(menu), "data": menu}

@app.get("/menu/summary")
def menu_summary():
    available = sum(1 for i in menu if i["is_available"])
    unavailable = len(menu) - available
    categories = list(set(i["category"] for i in menu))
    return {
        "total": len(menu),
        "available": available,
        "unavailable": unavailable,
        "categories": categories
    }

# ----------------------
# DAY 3 FILTER (BEFORE ID)
# ----------------------
@app.get("/menu/filter")
def filter_menu(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None
):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return {"count": len(result), "data": result}

# ----------------------
# DAY 6 (ALL BEFORE {id})
# ----------------------
@app.get("/menu/search")
def search(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    if not result:
        return {"message": "No items found"}
    return {"total_found": len(result), "data": result}

@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    reverse = True if order == "desc" else False
    result = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_by": sort_by, "order": order, "data": result}

@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    data = menu[start:start + limit]
    total_pages = (len(menu) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": len(menu),
        "total_pages": total_pages,
        "data": data
    }

@app.get("/menu/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    data = result[start:start + limit]

    return {
        "total": len(result),
        "page": page,
        "data": data
    }

# ----------------------
# GET BY ID (ALWAYS LAST)
# ----------------------
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/orders")
def get_orders():
    return {"total_orders": len(orders), "data": orders}

# ----------------------
# DAY 2 + 3
# ----------------------
class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=10)
    order_type: str = "delivery"

def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None

def calculate_bill(price, quantity, order_type):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["is_available"]:
        raise HTTPException(status_code=400, detail="Item not available")

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

# ----------------------
# DAY 4 CRUD
# ----------------------
class NewMenuItem(BaseModel):
    name: str = Field(min_length=2)
    price: int = Field(gt=0)
    category: str
    is_available: bool = True

@app.post("/menu")
def add_menu(item: NewMenuItem, response: Response):
    for m in menu:
        if m["name"].lower() == item.name.lower():
            raise HTTPException(status_code=400, detail="Duplicate item")

    new_item = item.dict()
    new_item["id"] = len(menu) + 1
    menu.append(new_item)

    response.status_code = 201
    return new_item

@app.put("/menu/{item_id}")
def update_menu(item_id: int, price: Optional[int] = None, is_available: Optional[bool] = None):
    item = find_menu_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if price is not None:
        item["price"] = price
    if is_available is not None:
        item["is_available"] = is_available

    return item

@app.delete("/menu/{item_id}")
def delete_menu(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    menu.remove(item)
    return {"message": f"{item['name']} deleted"}

# ----------------------
# DAY 5 CART
# ----------------------
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)
    if not item or not item["is_available"]:
        raise HTTPException(status_code=400, detail="Invalid item")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Updated cart"}

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Added to cart"}

@app.get("/cart")
def get_cart():
    total = 0
    result = []

    for c in cart:
        item = find_menu_item(c["item_id"])
        cost = item["price"] * c["quantity"]
        total += cost
        result.append({"item": item["name"], "quantity": c["quantity"], "cost": cost})

    return {"cart": result, "grand_total": total}

@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Removed"}
    raise HTTPException(status_code=404, detail="Not found")

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart empty")

    result = []
    total = 0

    for c in cart:
        item = find_menu_item(c["item_id"])
        price = item["price"] * c["quantity"]

        new_order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": item["name"],
            "quantity": c["quantity"],
            "total_price": price
        }

        result.append(new_order)
        total += price
        orders.append(new_order)
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": result, "grand_total": total}