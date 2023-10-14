from dataclasses import dataclass
from decimal import ROUND_DOWN, Decimal
from enum import Enum

from supermarket_pricing.exceptions import InvalidProductPriceException


class Price(Decimal):
    """
    SubClass of Decimal which formats the value as a two decimal price in pounds (£)
    Overrides __add__ __sub__ and __mul__ to ensure arithmatic operations result in a Price
    """

    def __str__(self):
        return f"£{self.quantize(Decimal('00.00'), rounding=ROUND_DOWN):.2f}"

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
    """
    SubClass of Decimal which formats the value as a three decimal value
    """

    def __str__(self):
        return f"{self.quantize(Decimal('0.000'), rounding=ROUND_DOWN):.3f}"


class PricingUnits(str, Enum):
    UNIT = "unit"
    KG = "kg"


@dataclass
class Product:
    """
    Represents a product with name and price, defaults to be priced by unit
    Does not allow for prices to be more granualr than 2 decimal places
    """

    name: str
    price: Price
    pricing_unit = PricingUnits.UNIT

    def __post_init__(self):
        if (
            self.price.as_tuple().exponent < -2
        ):  # Eventhough this can be rounded down, it's likely a mistake if more than 2 decimal places are specified
            raise InvalidProductPriceException(
                f"Invalid product price {self.price}: must not have more than 2 decimal places"
            )


@dataclass
class ProductByKg(Product):
    """
    Represents a product with name and price, prices by kg
    """

    pricing_unit = PricingUnits.KG
