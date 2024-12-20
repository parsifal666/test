from collections import namedtuple

class Product(namedtuple('Product', ['name', 'price', 'category'])):
    __slots__ = ()
    def discount_price(self, discount_percent):
        return self.price * (1 - discount_percent / 100)

class User(namedtuple('User', ['username', 'email', 'age'])):
    __slots__ = ()
    def is_adult(self):
        return self.age >= 18

if __name__ == "__main__":
    product = Product(name="Laptop", price=1000.0, category="Electronics")
    user = User(username="john_doe", email="john@example.com", age=25)

    print(product.discount_price(10))
    print(user.is_adult())
