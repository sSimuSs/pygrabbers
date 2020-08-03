import requests
from parser import adding


product_key = input("Product key(s)? :")
category = None

if "," in product_key:
    keys = product_key.split(",")
else:
    keys = [product_key]

for key in keys:
    product = requests.get('https://catalog.api.onliner.by/products/' + str(key)).json()
    if "parent_key" in product and product['parent_key'] != "":
        print("Adding parent product")
        parent_product = requests.get('https://catalog.api.onliner.by/products/' + str(product['parent_key'])).json()
        parent = adding(parent_product, category=category)
    else:
        parent = None
    print(adding(product, category=category, parent=parent))