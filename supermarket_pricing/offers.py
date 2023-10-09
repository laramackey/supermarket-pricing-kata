from abc import ABC, abstractmethod
from typing import Dict, List, Type

from supermarket_pricing.product import Product


class Offer(ABC):
    @abstractmethod
    def is_eligible(self, product_quantities: Dict[str, float]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def offer_amount(self, product_quantities: Dict[str, float]) -> float:
        raise NotImplementedError

    def check_and_apply(self, product_quantities: Dict[str, float]) -> float:
        if self.is_eligible(product_quantities):
            return round(self.offer_amount(product_quantities), 2)
        return 0


class ThreeForTwo(Offer):
    def __init__(self, eligible_product: Product | type[Product]) -> None:
        self.eligible_product = eligible_product

    def is_eligible(self, product_quantities: Dict[str, float]) -> bool:
        return product_quantities.get(self.eligible_product.name, 0) > 3

    def offer_amount(self, product_quantities: Dict[str, float]) -> float:
        number_of_offers = product_quantities[self.eligible_product.name] // 3
        return number_of_offers * self.eligible_product.price


class TwoForPrice(Offer):
    def __init__(self, eligible_product: Product | type[Product], offer_price: float) -> None:
        self.eligible_product = eligible_product
        self.offer_price = offer_price

    def is_eligible(self, product_quantities: Dict[str, float]) -> bool:
        return product_quantities.get(self.eligible_product.name, 0) > 2

    def offer_amount(self, product_quantities: Dict[str, float]) -> float:
        number_of_offers = product_quantities[self.eligible_product.name] // 2
        saving_per_offer = (self.eligible_product.price * 2) - self.offer_price
        return number_of_offers * saving_per_offer


class ThreeFromSetForPrice(Offer):
    def __init__(self, eligible_products: List[Product | type[Product]], offer_price: float) -> None:
        self.eligible_products = eligible_products
        self.offer_price = offer_price
        self.product_list: List[Product | Type[Product]] = []
        self.eligible_product_count = 0

    def is_eligible(self, product_quantities: Dict[str, float]) -> bool:
        eligible_product_names = [product.name for product in self.eligible_products]
        found_products = {key: value for key, value in product_quantities.items() if key in eligible_product_names}
        products_sorted_by_price = sorted(self.eligible_products, key=lambda product: product.price)
        self.product_list = [
            product for product in products_sorted_by_price for _ in range(int(found_products.get(product.name, 0)))
        ]
        self.eligible_product_count = len(self.product_list)
        return self.eligible_product_count > 3

    def offer_amount(self, _product_quantities: Dict[str, float]) -> float:
        number_of_offers = self.eligible_product_count // 3
        # Discount the cheapest products in the deal
        discounted_products = self.product_list[: number_of_offers * 3]
        pre_discounted_price = sum(product.price for product in discounted_products)
        return pre_discounted_price - (number_of_offers * self.offer_price)
