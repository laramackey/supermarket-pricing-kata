from typing import Dict

from supermarket_pricing.product_catalogue import product_catalogue


class ShoppingCart:
    def __init__(self) -> None:
        self.products: Dict[str, int] = {}

    def add_product(self, product_name: str):
        if product := product_catalogue.get(product_name):
            self.products[product_name] = self.products.get(product_name, 0) + 1
            print(product.price)
        else:
            raise Exception("Unexpected Item in Bagging Area")

    @property
    def total(self):
        total = 0
        for name, quantity in self.products.items():
            total += product_catalogue.get(name).price * quantity
        return total
