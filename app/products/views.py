from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def list_products():
    products = [
        {"name": "Ноутбук", "price": 35000},
        {"name": "Смартфон", "price": 25000},
        {"name": "Навушники", "price": 2000},
    ]
    return render_template("products/product.html", products=products)
