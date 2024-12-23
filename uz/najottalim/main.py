import requests
import sqlite3
import threading
import json

def save_to_database():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('products', [])
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            price REAL,
            brand TEXT,
            category TEXT
        )
        ''')
        for product in data:
            cursor.execute('''
            INSERT OR REPLACE INTO products (id, title, description, price, brand, category)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product.get('id'),
                product.get('title'),
                product.get('description'),
                product.get('price'),
                product.get('brand', 'Unknown'),
                product.get('category', 'Uncategorized')
            ))
        conn.commit()
        conn.close()

def save_to_json_file():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open('products.json', 'w') as file:
            json.dump(data, file, indent=4)

thread1 = threading.Thread(target=save_to_database)
thread2 = threading.Thread(target=save_to_json_file)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
