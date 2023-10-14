from typing import Union

from supermarket_pricing.product import Price
from supermarket_pricing.shopping_cart import ShoppingCart


def print_receipt_row(description: str, price: Union[str, Price] = "") -> None:
    """
    Print a single row of the receipt table.

    Args:
        description (str): The description of the line item.
        price (Union[str, Price]): The price of the line item, can be blank.
    """
    print("|", description.ljust(20), "|", str(price).rjust(6), "|")


def print_receipt(cart: ShoppingCart) -> None:
    """
    Print the itemized receipt for a shopping cart, including sub total, savings, and total amount.

    Args:
        cart (ShoppingCart): The shopping cart object.
    """
    for product in cart.products_in_cart:
        product_name = product.name.capitalize()
        if product.price_per_kg:
            print_receipt_row(product_name)
            print_receipt_row(f"{str(product.quantity)} kg @ {str(product.price_per_kg)}/kg", product.price)
        else:
            quantity = (
                f" x {product.quantity}" if product.quantity != 1 else ""
            )  # Only display product quantity if it's not 1
            print_receipt_row(f"{product_name}{quantity}", product.price)
    if cart.savings:
        print_receipt_row("**Sub-total**", cart.sub_total)
        print_receipt_row("**Savings**")
        for offer in cart.applied_offers:
            print_receipt_row(offer.description.capitalize(), f"-{str(offer.offer_amount)}")
        print_receipt_row("**Total savings**", cart.savings)
    print_receipt_row("**Total to Pay**", cart.total)
