from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List, Tuple, Type

from supermarket_pricing.product import Price, Product


class Offer(ABC):
    """
    Abstract class for any offer, is_eligible and offer_amount must be implemented
    """

    def __init__(self) -> None:
        """
        Initialize an offer with a description of the offer.
        """
        self.short_description = ""

    @abstractmethod
    def is_eligible(self, product_quantities: Dict[str, Decimal]) -> bool:
        """
        Check if the offer is eligible for the given product quantities.

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            bool: True if the offer is eligible, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def offer_amount(self, product_quantities: Dict[str, Decimal]) -> Price:
        """
        Calculate the amount of discounted for the offer.

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            Price: The amount of discount or savings.
        """
        raise NotImplementedError

    def check_and_apply(self, product_quantities: Dict[str, Decimal]) -> Price:
        """
        Check if the offer is eligible and apply it to the product quantities.

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            Price: The amount of discount or savings if the offer is eligible, or Price(0) if not eligible.
        """
        if self.is_eligible(product_quantities):
            return self.offer_amount(product_quantities)
        return Price(0)


class ThreeForTwo(Offer):
    """
    Three for the price of two offer
    """

    def __init__(self, eligible_product: Product) -> None:
        """
        Args:
        eligible_product (Product): The eligible product for this offer.
        """
        self.eligible_product = eligible_product
        self.short_description = f"{eligible_product.name} 3 for 2"

    def is_eligible(self, product_quantities: Dict[str, Decimal]) -> bool:
        """
        Checks if there is more than three products to confirm elibility.

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            bool: True if the offer is eligible, False otherwise.
        """
        return product_quantities.get(self.eligible_product.name, 0) >= 3

    def offer_amount(self, product_quantities: Dict[str, Decimal]) -> Price:
        """
        Calculate how many sets of three there are, and how much savings there are based on the product price.

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            Price: The amount of discount or savings.
        """
        number_of_offers = product_quantities[self.eligible_product.name] // 3
        product_price: Price = self.eligible_product.price
        return Price(number_of_offers * product_price)


class TwoForPrice(Offer):
    """
    Two for a given price of two offer
    """

    def __init__(self, eligible_product: Product, offer_price: Price) -> None:
        """
        Args:
        eligible_product (Product): The eligible product for this offer.
        offer_price (Price): The price of the two products bought together
        """
        self.eligible_product = eligible_product
        self.offer_price = offer_price
        self.short_description = f"{eligible_product.name} 2 for {str(offer_price)}"

    def is_eligible(self, product_quantities: Dict[str, Decimal]) -> bool:
        """
        Checks if there is more than two products to confirm elibility

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            bool: True if the offer is eligible, False otherwise.
        """
        return product_quantities.get(self.eligible_product.name, 0) >= 2

    def offer_amount(self, product_quantities: Dict[str, Decimal]) -> Price:
        """
        Calculate how many sets of two there are,
        and how much savings there are based on the product price minus the deal price

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            Price: The amount of discount or savings.
        """
        number_of_offers = product_quantities[self.eligible_product.name] // 2
        saving_per_offer = (self.eligible_product.price * 2) - self.offer_price
        return Price(number_of_offers * saving_per_offer)


class ThreeFromSetForPrice(Offer):
    """
    Three items from a set for a given price, discounts the cheapest items in the set
    """

    def __init__(self, eligible_products: Tuple[Product, ...], offer_price: Decimal, offer_category: str) -> None:
        """
        Args:
        eligible_product (Tuple[Product, ...]): The eligible products for this offer.
        offer_price (Price): The price of the two products bought together
        offer_category (str): The category of products in the set, used for the offer description
        """
        self.eligible_products = eligible_products
        self.offer_price = offer_price
        self.short_description = f"{offer_category} 3 for {str(offer_price)}"
        self.product_list: List[Product | Type[Product]] = []
        self.eligible_product_count = 0

    def is_eligible(self, product_quantities: Dict[str, Decimal]) -> bool:
        """
        Checks if there is more than three products amongst the set to confirm elibility

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            bool: True if the offer is eligible, False otherwise.
        """
        eligible_product_names = [product.name for product in self.eligible_products]
        found_products = {key: value for key, value in product_quantities.items() if key in eligible_product_names}
        products_sorted_by_price = sorted(self.eligible_products, key=lambda product: product.price)
        self.product_list = [
            product for product in products_sorted_by_price for _ in range(int(found_products.get(product.name, 0)))
        ]  # Store list of eligible products, to be used to calculate offer amount
        self.eligible_product_count = len(
            self.product_list
        )  # Store count of eligible products, to be used to calculate offer amount
        return self.eligible_product_count >= 3

    def offer_amount(self, _product_quantities: Dict[str, Decimal]) -> Price:
        """
        Calculate how many sets of three there are,
        and how much savings there are based on the product price minus the deal price.
        Discounts the cheapest products in the deal, as the products in the set can have different prices

        Args:
            product_quantities (dict): A dictionary of product names to quantities.

        Returns:
            Price: The amount of discount or savings.
        """
        number_of_offers = self.eligible_product_count // 3
        discounted_products = self.product_list[: number_of_offers * 3]
        pre_discounted_price = sum(product.price for product in discounted_products)
        return Price(pre_discounted_price - (number_of_offers * self.offer_price))
