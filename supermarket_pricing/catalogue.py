from typing import Dict, Type, Union

from supermarket_pricing.offers import ThreeForTwo, ThreeFromSetForPrice, TwoForPrice
from supermarket_pricing.product import Product, ProductByKg

PRODUCT_CATALOGUE: Dict[str, Union[Product, Type[Product]]] = {
    "beans": Product("beans", 0.5),
    "coke": Product("coke", 0.7),
    "onions": ProductByKg("onions", 0.29),
    "arbor ale": Product("arbor ale", 2.2),
    "kaleidoscope": Product("kaleidoscope", 2.5),
    "butcombe": Product("butcombe", 2.1),
}


OFFERS = [
    ThreeForTwo(PRODUCT_CATALOGUE["beans"]),
    TwoForPrice(PRODUCT_CATALOGUE["coke"], 1.0),
    ThreeFromSetForPrice(
        [PRODUCT_CATALOGUE["arbor ale"], PRODUCT_CATALOGUE["kaleidoscope"], PRODUCT_CATALOGUE["butcombe"]], 6.0
    ),
]
