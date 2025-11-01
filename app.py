from flask import Flask, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SHOP_NAME = os.getenv("SHOPIFY_STORE_NAME")
API_KEY = os.getenv("SHOPIFY_API_KEY")
ACCESS_TOKEN = os.getenv("SHOPIFY_PASSWORD")

@app.route('/')
def index():
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-10/products.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"❌ Error: {response.status_code} — {response.text}"

    products = response.json().get("products", [])
    product_data = []

    for product in products:
        for variant in product["variants"]:
            product_data.append({
                "title": product["title"],
                "variant": variant["title"],
                "price": variant["price"],
                "inventory": variant["inventory_quantity"]
            })

    return render_template("index.html", products=product_data)

if __name__ == '__main__':
    app.run(debug=True)
