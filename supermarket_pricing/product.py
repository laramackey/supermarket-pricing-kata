from dataclasses import dataclass
from enum import Enum


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


@dataclass
class Product:
    name: str
    price: float
    pricing_unit = PricingUnits.UNIT


@dataclass
class ProductByKg(Product):
    pricing_unit = PricingUnits.KG
