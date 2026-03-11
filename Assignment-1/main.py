from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'Refrigerator',   'price':  9999, 'category': 'Furniture',  'in_stock': True },
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Keyboard',          'price':  699, 'category': 'Electronics',  'in_stock': False },
    {'id': 6, 'name': 'Table',   'price': 499, 'category': 'Furniture',  'in_stock': False },
    {'id': 7, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
]

# ── Helper function to convert string to boolean ─────────────
def str_to_bool(v: Optional[str]):
    if v is None:
        return None
    return v.lower() in ['true', '1', 'yes']

# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── Endpoint 2 — Filter products ─────────────────────────────
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationery'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock: str = Query(None, description='True = in stock only')
):
    in_stock_bool = str_to_bool(in_stock)
    result = products  # start with all products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock_bool is not None:
        result = [p for p in result if p['in_stock'] == in_stock_bool]

    return {'filtered_products': result, 'count': len(result)}
@app.get('/store/summary')
def store_summary():
    total_products = len(products)
    in_stock_count = sum(1 for p in products if p['in_stock'])
    out_of_stock_count = total_products - in_stock_count
    categories = list({p['category'] for p in products})  # unique categories

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }
@app.get('/products/search/{keyword}')
def search_products(keyword: str):
    keyword_lower = keyword.lower()
    matched = [p for p in products if keyword_lower in p['name'].lower()]

    if not matched:
        return {"message": "No products matched your search"}

    return {"matched_products": matched, "total_matches": len(matched)}
@app.get('/products/deals')
def product_deals():
    if not products:
        return {"message": "No products available"}

    # Find the product with the lowest price
    best_deal = min(products, key=lambda p: p['price'])

    # Find the product with the highest price
    premium_pick = max(products, key=lambda p: p['price'])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }

# ── Endpoint 3 — Return one product by its ID ────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}