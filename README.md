# 🍔 FastAPI Food Delivery Backend System

## 📌 Project Overview
This project is a complete backend system built using **FastAPI** as part of my internship training.  
It simulates a real-world **Food Delivery Application**, where users can browse menu items, place orders, manage a cart, and perform advanced operations like search, sorting, and pagination.

---

## 🎯 Objectives
- Build RESTful APIs using FastAPI  
- Implement request validation using Pydantic  
- Perform CRUD operations  
- Design multi-step workflows  
- Implement advanced features like filtering, searching, sorting, and pagination  

---

## 🛠️ Tech Stack
- Python  
- FastAPI  
- Pydantic  
- Uvicorn 

---

## 📂 Project Structure
fastapi-food-delivery-app/

│

├── main.py

├── requirements.txt

├── README.md

└── screenshots/

    │
    
    └── Outputs 1 - 20
    


---

# 📊 Implementation (Question-wise)

## 🟢 Day 1 — Basic GET APIs (Q1–Q5)

### Q1 — Home Route
- Endpoint: `GET /`
- Returns welcome message

### Q2 — Get All Menu
- Endpoint: `GET /menu`
- Returns all menu items with total count

### Q3 — Get Item by ID
- Endpoint: `GET /menu/{item_id}`
- Returns item or error if not found

### Q4 — Get Orders
- Endpoint: `GET /orders`
- Returns all orders (initially empty)

### Q5 — Menu Summary
- Endpoint: `GET /menu/summary`
- Returns total, available, unavailable items and categories

---

## 🔵 Day 2 & 3 — POST + Validation + Helpers (Q6–Q10)

### Q6 — Create Order with Validation
- Endpoint: `POST /orders`
- Uses Pydantic validation (min_length, gt, etc.)

### Q7 — Helper Functions
- `find_menu_item()` → fetch item  
- `calculate_bill()` → calculate total  

### Q8 — Create Order (Success Case)
- Valid order creation
- Generates `order_id`

### Q9 — Delivery vs Pickup Logic
- Adds ₹30 for delivery  
- No charge for pickup  

### Q10 — Filter Menu
- Endpoint: `GET /menu/filter`
- Filters by category, price, availability  

---

## 🟠 Day 4 — CRUD Operations (Q11–Q13)

### Q11 — Add Menu Item
- Endpoint: `POST /menu`
- Adds new item with validation  

### Q12 — Update Menu Item
- Endpoint: `PUT /menu/{item_id}`
- Updates price or availability  

### Q13 — Delete Menu Item
- Endpoint: `DELETE /menu/{item_id}`
- Removes item from menu  

---

## 🟢 Day 5 — Multi-Step Workflow (Q14–Q15)

### Q14 — Cart System
- Endpoint: `POST /cart/add`
- Endpoint: `GET /cart`
- Add items & view cart with total  

### Q15 — Checkout
- Endpoint: `POST /cart/checkout`
- Converts cart to orders and clears cart  

---

## 🟣 Day 6 — Advanced APIs (Q16–Q20)

### Q16 — Search Menu
- Endpoint: `GET /menu/search`
- Search by name or category  

### Q17 — Sort Menu
- Endpoint: `GET /menu/sort`
- Sort by price, name, category  

### Q18 — Pagination
- Endpoint: `GET /menu/page`
- Returns paginated results  

### Q19 — Orders List
- Endpoint: `GET /orders`
- Shows all created orders  

### Q20 — Combined Browse API
- Endpoint: `GET /menu/browse`
- Combines filter + sort + pagination  

---

## ▶️ How to Run

### Install dependencies
```cmd
pip install -r requirements.txt
```

### Run server
```cmd
uvicorn main:app --reload
```



### Open Swagger

http://127.0.0.1:8000/docs


---

## 🧪 Testing
- All APIs tested in Swagger UI  
- Screenshots for all 20 questions included  

---

## 📸 Screenshots
- Located in `screenshots/` folder  
- Each screenshot corresponds to Q1–Q20  

---

## 📈 Learning Outcomes
- API development using FastAPI  
- Data validation using Pydantic  
- Backend workflow design  
- Debugging route conflicts  
- Implementing real-world features  

---

## 🙏 Acknowledgment
I would like to thank **Innomatics Research Labs** for providing this opportunity to build a real-world backend project.

---

## 📌 Conclusion
This project demonstrates my ability to design and implement a complete backend system using FastAPI, covering all essential backend development concepts.
