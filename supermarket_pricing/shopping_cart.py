import math
from typing import Dict

from supermarket_pricing.catalogue import OFFERS, PRODUCT_CATALOGUE
from supermarket_pricing.exceptions import (
    InvalidProductException,
    ProductQuantityException,
)
from supermarket_pricing.product import PricingUnits


class ShoppingCart:
    def __init__(self) -> None:
        self.products: Dict[str, float] = {}

    def add_product(self, product_name: str, quantity: float = 1.0) -> None:
        if product := PRODUCT_CATALOGUE.get(product_name):
            if product.pricing_unit == PricingUnits.UNIT and not float(quantity).is_integer():
                raise ProductQuantityException(f"Product quantity for {product_name} must be specified in integers")
            self.products[product_name] = self.products.get(product_name, 0) + quantity
            print(f"| {product_name} | {product.price}")
        else:
            raise InvalidProductException("Unexpected Item in Bagging Area")

    @property
    def sub_total(self) -> float:
        total = 0.0
        for name, quantity in self.products.items():
            product = PRODUCT_CATALOGUE[name]
            if product.pricing_unit == PricingUnits.UNIT:
                total += product.price * quantity
            elif product.pricing_unit == PricingUnits.KG:
                total += self.__round_down_price(product.price * quantity)
        return total

    @property
    def savings(self) -> float:
        return sum(offer.check_and_apply(self.products) for offer in OFFERS)

    @property
    def total(self) -> float:
        return self.sub_total - self.savings

    @staticmethod
    def __round_down_price(price: float) -> float:
        minimum_price = 0.01
        return max(minimum_price, math.floor((price) * 100) / 100)
