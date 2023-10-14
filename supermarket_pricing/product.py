from dataclasses import dataclass
from decimal import Decimal, getcontext
from enum import Enum

from supermarket_pricing.exceptions import InvalidProductException


class Price(Decimal):
    def __str__(self):
        getcontext().rounding = "ROUND_DOWN"
        return f"£{self.quantize(Decimal('00.00')):.2f}"

    def __add__(self, other):
        result = super().__add__(other)
        if isinstance(other, Price):
            return Price(result)
        return Price(super(Price, result))

    def __sub__(self, other):
        result = super().__sub__(other)
        return Price(result)

    def __mul__(self, other):
        result = super().__mul__(other)
        return Price(result)


class Weight(Decimal):
    def __str__(self):
        getcontext().rounding = "ROUND_DOWN"
        return f"{self.quantize(Decimal('0.000')):.3f}"


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


@dataclass
class Product:
    name: str
    price: Price
    pricing_unit = PricingUnits.UNIT

    def __post_init__(self):
        if (
            self.price.as_tuple().exponent < -2
        ):  # Eventhough this can be rounded down, it's likely a mistake if more than 2 decimal places are specified
            raise InvalidProductException(
                f"Invalid product price {self.price}: must not have more than 2 decimal places"
            )


@dataclass
class ProductByKg(Product):
    pricing_unit = PricingUnits.KG
