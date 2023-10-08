from typing import Dict, Type, Union

from supermarket_pricing.offers import ThreeForTwo
from supermarket_pricing.product import Product, ProductByKg

PRODUCT_CATALOGUE: Dict[str, Union[Product, Type[Product]]] = {
    "beans": Product("beans", 0.5),
    "coke": Product("coke", 0.7),
    "onions": ProductByKg("onions", 0.29),
    "arbor ale": Product("arbor ale", 2.2, "ale"),
    "kaleidoscope": Product("kaleidoscope", 2.5, "ale"),
    "butcombe": Product("butcombe", 2.1, "ale"),
}


OFFERS = [ThreeForTwo("beans")]
