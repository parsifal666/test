import requests
import sqlite3
import json
from threading import Thread

def save_to_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY, 
                        title TEXT, 
                        description TEXT, 
                        price REAL, 
                        category TEXT)''')
    response = requests.get('https://dummyjson.com/products')
    products = response.json().get('products', [])
    for product in products:
        cursor.execute('SELECT id FROM products WHERE id = ?', (product['id'],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO products (id, title, description, price, category) 
                               VALUES (?, ?, ?, ?, ?)''',
                               (product['id'], product['title'], product['description'],
                                product['price'], product['category']))
    conn.commit()
    conn.close()


def save_to_json():
    response = requests.get('https://dummyjson.com/products')
    products = response.json().get('products', [])
    with open('products.json', 'w') as file:
        json.dump(products, file)

t1 = Thread(target=save_to_database)
t2 = Thread(target=save_to_json)

t1.start()
t2.start()

t1.join()
t2.join()
