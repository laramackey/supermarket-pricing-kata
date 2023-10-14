from typing import Union

from supermarket_pricing.shopping_cart import ShoppingCart


def print_receipt_row(description: str, price: Union[str, float] = ""):
    formatted_price = f"£{price:.2f}" if isinstance(price, float) else ""
    print("|", description.capitalize().ljust(20), "|", formatted_price.rjust(6), "|")


def print_receipt(cart: ShoppingCart):
    for item in cart.products_in_cart:
        if item.price_per_kg:
            print_receipt_row(item.name)
            print_receipt_row(f"{item.quantity} kg @ £{item.price_per_kg:.2f}/kg", item.price)
        else:
            quantity = f" x {item.quantity}" if item.quantity != 1 else ""
            print_receipt_row(f"{item.name}{quantity}", item.price)
