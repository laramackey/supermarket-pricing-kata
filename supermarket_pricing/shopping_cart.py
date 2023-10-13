import math
from collections import namedtuple
from typing import Dict, List

from supermarket_pricing.catalogue import OFFERS, PRODUCT_CATALOGUE
from supermarket_pricing.exceptions import (
    InvalidProductException,
    ProductQuantityException,
)
from supermarket_pricing.offers import Offer
from supermarket_pricing.product import PricingUnits, Product

AddedProduct = namedtuple("AddedProduct", "name quantity price")
AppliedOffer = namedtuple("AppliedOffer", "description offer_amount")


class ShoppingCart:
    def __init__(
        self,
        product_catalogue: Dict[str, Product] = PRODUCT_CATALOGUE,
        offers_catalogue: List[Offer] = OFFERS,
    ) -> None:
        self.product_catalogue = product_catalogue
        self.offers_catalogue = offers_catalogue
        self.product_quantities: Dict[str, float] = {}
        self.products_in_cart: List[AddedProduct] = []
        self.applied_offers: List[AppliedOffer] = []

    def add_product(self, product_name: str, quantity: float = 1.0) -> None:
        if product := self.product_catalogue.get(product_name):
            if product.pricing_unit == PricingUnits.UNIT and not float(quantity).is_integer():
                raise ProductQuantityException(f"Product quantity for {product_name} must be specified in integers")
            self.product_quantities[product_name] = self.product_quantities.get(product_name, 0) + quantity
            self.products_in_cart.append(
                AddedProduct(product, quantity, self.__get_product_quantity_price(product, quantity))
            )
        else:
            raise InvalidProductException("Unexpected Item in Bagging Area")

    def __get_product_quantity_price(self, product: Product, quantity: float) -> float:
        if product.pricing_unit == PricingUnits.UNIT:
            return product.price * quantity
        elif product.pricing_unit == PricingUnits.KG:
            return self.__round_down_price(product.price * quantity)

    @property
    def sub_total(self) -> float:
        return sum(product.price for product in self.products_in_cart)

    @property
    def savings(self) -> float:
        savings = 0.0
        applied_offers: List[AppliedOffer] = []
        for offer in self.offers_catalogue:
            if (offer_amount := offer.check_and_apply(self.product_quantities)) > 0:
                applied_offers.append(AppliedOffer(offer.short_description, offer_amount))
                savings += offer_amount
        self.applied_offers = applied_offers
        return savings

    @property
    def total(self) -> float:
        return self.sub_total - self.savings

    @staticmethod
    def __round_down_price(price: float) -> float:
        minimum_price = 0.01
        return max(minimum_price, math.floor((price) * 100) / 100)
