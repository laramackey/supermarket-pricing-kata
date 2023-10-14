from typing import Union

from supermarket_pricing.product import Price
from supermarket_pricing.shopping_cart import ShoppingCart


def print_receipt_row(description: str, price: Union[str, Price] = "") -> None:
    print("|", description.ljust(20), "|", str(price).rjust(6), "|")


def print_receipt(cart: ShoppingCart) -> None:
    for product in cart.products_in_cart:
        product_name = product.name.capitalize()
        if product.price_per_kg:
            print_receipt_row(product_name)
            print_receipt_row(f"{str(product.quantity)} kg @ {str(product.price_per_kg)}/kg", product.price)
        else:
            quantity = f" x {product.quantity}" if product.quantity != 1 else ""
            print_receipt_row(f"{product_name}{quantity}", product.price)
    if cart.savings:
        print_receipt_row("**Sub-total**", cart.sub_total)
        print_receipt_row("**Savings**")
        for offer in cart.applied_offers:
            print_receipt_row(offer.description.capitalize(), f"-{str(offer.offer_amount)}")
        print_receipt_row("**Total savings**", cart.savings)
    print_receipt_row("**Total to Pay**", cart.total)
