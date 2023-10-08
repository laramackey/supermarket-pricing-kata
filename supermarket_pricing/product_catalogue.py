from enum import Enum
from typing import Dict, Type, Union


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


class Product:
    def __init__(self, name: str, price: float, product_category: str = None) -> None:
        self.name = name
        self.price = price
        self.pricing_unit = PricingUnits.UNIT
        self.product_category = product_category


class ProductByKg(Product):
    def __init__(self, name: str, price: float) -> None:
        super().__init__(name, price)
        self.pricing_unit = PricingUnits.KG


PRODUCT_CATALOGUE: Dict[str, Union[Product, Type[Product]]] = {
    "beans": Product("beans", 0.5),
    "coke": Product("coke", 0.7),
    "onions": ProductByKg("onions", 0.29),
    "arbor ale": Product("arbor ale", 2.2, "ale"),
    "kaleidoscope": Product("kaleidoscope", 2.5, "ale"),
    "butcombe": Product("butcombe", 2.1, "ale"),
}
