from supermarket_pricing.shopping_cart import ShoppingCart


def print_receipt(cart: ShoppingCart):
    for item in cart.products_in_cart:
        print(f"{item.name}: {item.price}")
