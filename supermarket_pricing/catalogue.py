from typing import Dict, List

from supermarket_pricing.offers import (
    Offer,
    ThreeForTwo,
    ThreeFromSetForPrice,
    TwoForPrice,
)
from supermarket_pricing.product import Price, Product, ProductByKg

PRODUCT_CATALOGUE: Dict[str, Product] = {
    "beans": Product("beans", Price("0.5")),
    "coke": Product("coke", Price("0.7")),
    "onions": ProductByKg("onions", Price("0.29")),
    "oranges": ProductByKg("oranges", Price("1.99")),
    "arbor ale": Product("arbor ale", Price("2.2")),
    "kaleidoscope": Product("kaleidoscope", Price("2.5")),
    "butcombe": Product("butcombe", Price("2.1")),
}


OFFERS: List[Offer] = [
    ThreeForTwo(PRODUCT_CATALOGUE["beans"]),
    TwoForPrice(PRODUCT_CATALOGUE["coke"], Price("1")),
    ThreeFromSetForPrice(
        [PRODUCT_CATALOGUE["arbor ale"], PRODUCT_CATALOGUE["kaleidoscope"], PRODUCT_CATALOGUE["butcombe"]],
        Price("6"),
        "ales",
    ),
]
