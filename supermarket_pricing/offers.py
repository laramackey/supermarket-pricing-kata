import math
from abc import ABC, abstractmethod
from typing import Dict

from supermarket_pricing.product_catalogue import PRODUCT_CATALOGUE


class Offer(ABC):
    def __init__(self, eligible_product: str) -> None:
        self.eligible_product = eligible_product

    @abstractmethod
    def is_eligible(self, products: Dict[str, float]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def offer_amount(self, products: Dict[str, float]) -> float:
        raise NotImplementedError

    def check_and_apply(self, products: Dict[str, float]) -> float:
        if self.is_eligible(products):
            return self.offer_amount(products)
        return 0


class ThreeForTwo(Offer):
    def is_eligible(self, products: Dict[str, float]) -> bool:
        return products.get(self.eligible_product, 0) > 3

    def offer_amount(self, products: Dict[str, float]) -> float:
        number_of_offers = math.floor(products[self.eligible_product] / 3)
        return number_of_offers * PRODUCT_CATALOGUE[self.eligible_product].price


OFFERS = [ThreeForTwo("beans")]