import math
from typing import Dict

from supermarket_pricing.product_catalogue import PricingUnits, product_catalogue


class ShoppingCart:
    def __init__(self) -> None:
        self.products: Dict[str, float] = {}

    def add_product(self, product_name: str, quantity: float = 1.0):
        if product := product_catalogue.get(product_name):
            if product.pricing_unit == PricingUnits.UNIT and not quantity.is_integer():
                raise Exception("Product quantity must be specified in integers")
            self.products[product_name] = self.products.get(product_name, 0) + quantity
            print(f"| {product_name} | {product.price}")
        else:
            raise Exception("Unexpected Item in Bagging Area")

    @property
    def total(self):
        total = 0
        for name, quantity in self.products.items():
            product = product_catalogue.get(name)
            if product.pricing_unit == PricingUnits.UNIT:
                total += product.price * quantity
            elif product.pricing_unit == PricingUnits.KG:
                total += self.__round_down_price(product.price * quantity)
        return total

    @staticmethod
    def __round_down_price(price: float) -> float:
        minimum_price = 0.01
        return max(minimum_price, math.floor((price) * 100) / 100)
