from supermarket_pricing.shopping_cart import ShoppingCart


def test_get_total_for_one_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    assert cart.total == 0.5


def test_get_total_for_multiple_of_same_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("beans")
    cart.add_product("beans")
    assert cart.total == 1.5


def test_get_total_for_multiple_items():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("beans")
    cart.add_product("coke")
    assert cart.total == 1.7
