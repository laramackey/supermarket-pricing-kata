from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


@dataclass
class Product:
    name: str
    price: float
    product_type: Optional[str] = None
    pricing_unit = PricingUnits.UNIT


@dataclass
class ProductByKg(Product):
    pricing_unit = PricingUnits.KG
