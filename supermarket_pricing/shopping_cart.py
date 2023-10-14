from collections import namedtuple
from decimal import ROUND_DOWN, Decimal, InvalidOperation
from typing import Dict, List, Tuple

from supermarket_pricing.catalogue import OFFERS, PRODUCT_CATALOGUE
from supermarket_pricing.exceptions import (
    InvalidProductException,
    ProductQuantityException,
)
from supermarket_pricing.offers import Offer
from supermarket_pricing.product import Price, PricingUnits, Product, Weight

AddedProduct = namedtuple("AddedProduct", "name quantity price price_per_kg")
AppliedOffer = namedtuple("AppliedOffer", "description offer_amount")


class ShoppingCart:
    """
    Represents a ShoppingCart which items can be added to,
    and calculate the sub_total, savings and total from the items in the cart
    """

    def __init__(
        self,
        product_catalogue: Dict[str, Product] = PRODUCT_CATALOGUE,
        offers_catalogue: Tuple[Offer, ...] = OFFERS,
    ) -> None:
        """
        Initialize a shopping cart.

        Args:
            product_catalogue (dict): A dictionary of product names to Products that are available to buy.
            offers_catalogue (tuple): A tuple of Offers that can be applied.
        """
        self.product_catalogue = product_catalogue
        self.offers_catalogue = offers_catalogue
        self.product_quantities: Dict[str, Decimal] = {}
        self.products_in_cart: List[AddedProduct] = []
        self.applied_offers: List[AppliedOffer] = []

    def add_product(self, product_name: str, input_quantity: str = "1") -> None:
        """
        Add a product to the shopping cart.

        Args:
            product_name (str): The name of the product to add.
            input_quantity (str) [optional, default="1"]: The quantity of the product to add,
                must be a whole number if the product is priced per unit, and can be in decimals if priced by weight

        Raises:
            InvalidProductException: If the product is not found in the catalog.
            ProductQuantityException: If there is an issue with the input quantity.
        """
        if product := self.product_catalogue.get(product_name):
            quantity = self.__parse_quantity(input_quantity, product)
            self.product_quantities[product_name] = (
                self.product_quantities.get(product_name, 0) + quantity
            )  # Track product quantites for offer eligibility
            price_per_kg = product.price if product.pricing_unit == PricingUnits.KG else 0
            self.products_in_cart.append(
                AddedProduct(
                    product_name, quantity, self.__round_down_price(Price(product.price * quantity)), price_per_kg
                )
            )
        else:
            raise InvalidProductException("Unexpected Item in Bagging Area")

    @property
    def sub_total(self) -> Price:
        """
        Returns:
            Price: The total subtotal of the items in the shopping cart before offers.
        """
        return sum((product.price for product in self.products_in_cart), Price(0))

    @property
    def savings(self) -> Price:
        """
        Returns:
            Price: The total savings of all applicable offers.
        """
        savings: Price = Price(0.0)
        applied_offers: List[AppliedOffer] = []
        for offer in self.offers_catalogue:
            if (offer_amount := offer.check_and_apply(self.product_quantities)) > 0:
                applied_offers.append(
                    AppliedOffer(offer.short_description, offer_amount)
                )  # Store list of applied offers for receipt or audit
                savings += offer_amount
        self.applied_offers = applied_offers
        return savings

    @property
    def total(self) -> Price:
        """
        Returns:
            Price: The total of all items after offers.
        """
        return self.sub_total - self.savings

    def __parse_quantity(self, input_quantity: str, product: Product) -> Decimal:
        """
        Parse and validate the input quantity for a product.

        Args:
            input_quantity (str): The input quantity.
            product (Product): The product being added.

        Returns:
            Decimal: The parsed and validated quantity.

        Raises:
            ProductQuantityException: If there is an issue with the input quantity.
        """
        try:
            quantity = Weight(input_quantity) if product.pricing_unit == PricingUnits.KG else Decimal(input_quantity)
        except InvalidOperation:
            raise ProductQuantityException(f"Product quantity for {product.name} must be a valid number")
        if quantity <= 0:
            raise ProductQuantityException(f"Product quantity for {product.name} must be a positive value")
        if product.pricing_unit == PricingUnits.UNIT and not self.__decimal_is_int(quantity):
            raise ProductQuantityException(f"Product quantity for {product.name} must be specified in integers")
        return quantity

    @staticmethod
    def __decimal_is_int(number: Decimal) -> bool:
        """
        Check if a decimal number is an integer.
        Args:
            number (Decimal): The number to check.
        Returns:
            bool: True if the number is an integer, False otherwise.
        """
        return number.as_integer_ratio()[1] == 1

    @staticmethod
    def __round_down_price(price: Price) -> Price:
        """
        Round down a Price to two decimal places.

        Args:
            price (Price): The Price to round down.

        Returns:
            Price: The rounded down Price.
        """
        minimum_price = Price("0.01")
        return Price(max(minimum_price, price.quantize(Price("0.00"), rounding=ROUND_DOWN)))
