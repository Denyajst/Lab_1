#Variant 1
"""Розробити класи Покупець, Продавець, Замовлення, Товар. Реалізувати
логіку роботи площадки для торгівлі товарами. Продавець може мати
номенклатуру різних товарів, які продає. Покупець може оформити
покупку одного товару, при цьому у замовленні в графі доставки вказується
адреса покупця, а також з рахунку покупця на рахунок продавця
перераховується вартість товару. Одночасно можуть покупати товари
декілька покупців. Реалізувати блокування рахунку продавця під час його
поповнення. Пояснити доцільність такого підходу"""

import threading
import time


class Product:
    def __init__(self,name: str,price: float,quantity: int):
        self.name = name 
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.name}:\n Price:{self.price}\n Quantity:{self.quantity}"

class Seller:
    def __init__(self,name: str):
        self.name = name
        self.balance_lock = threading.Lock()
        self.seller_balance = 0
        self.seller_products = {}

    def add_product(self, product:Product):
        self.seller_products[product.name] = product
    
    def get_ptoducts(self):
        return self.seller_products
    
    def update_balance(self,amount):
        with self.balance_lock:
            self.seller_balance += amount

class Buyer:
    def __init__(self,name: str, address: str, balance: float):
        self.name = name 
        self.address = address
        self.balance = balance
    
    def make_order(self,seller:Seller ,product_name: str,):
        print("Please wait the order is being processed")
        time.sleep(3)
        if product_name in seller.get_ptoducts():
            product = seller.seller_products[product_name]
            if product.quantity == 0 or self.balance < product.price:
                print("Product not avalible")
            else:
                order = Order(self,seller,product)
                print(order)
                product.quantity -=1
                self.balance -= product.price
                seller.update_balance(product.price)
                print("Order success")
        else:
            print("Product not avalible")

class Order:
    def __init__(self, buyer: Buyer, seller: Seller, product: Product):
        self.buyer = buyer
        self.seller = seller
        self.product = product
    
    def __str__ (self):
        return(f"Order: {self.product.name}\n Address: {self.buyer.address}")

seller1 = Seller("Comfy")
product = Product("Phone", 12, 5)
seller1.add_product(product)

buyer1 = Buyer("Alice", "123 Street", 100)
buyer2 = Buyer("Mark", "41 Avenue", 13)

order1 = threading.Thread(target=buyer1.make_order, args=(seller1, "Phone"))
order2 = threading.Thread(target=buyer2.make_order, args=(seller1, "Phone"))
    
order1.start()
order2.start()

order1.join()
order2.join()
    

        