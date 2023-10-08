import math
from abc import ABC, abstractmethod
from typing import Dict

import supermarket_pricing.catalogue as catalogue


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
        return round(number_of_offers * catalogue.PRODUCT_CATALOGUE[self.eligible_product].price, 2)


class TwoForPrice(Offer):
    def __init__(self, eligible_product: str, offer_price: float) -> None:
        super().__init__(eligible_product)
        self.offer_price = offer_price

    def is_eligible(self, products: Dict[str, float]) -> bool:
        return products.get(self.eligible_product, 0) > 2

    def offer_amount(self, products: Dict[str, float]) -> float:
        number_of_offers = math.floor(products[self.eligible_product] / 2)
        saving_per_offer = (catalogue.PRODUCT_CATALOGUE[self.eligible_product].price * 2) - self.offer_price
        return round(number_of_offers * saving_per_offer, 2)
