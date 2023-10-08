from enum import Enum


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.pricing_unit = PricingUnits.UNIT


class ProductByKg(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.pricing_unit = PricingUnits.KG


product_catalogue = {
    "beans": Product("beans", 0.5),
    "coke": Product("coke", 0.7),
    "onions": ProductByKg("onions", 0.29),
}
