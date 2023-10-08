import pytest
from supermarket_pricing.exceptions import (
    InvalidProductException,
    ProductQuantityException,
)
from supermarket_pricing.shopping_cart import ShoppingCart


def test_get_total_for_one_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    assert cart.total == 0.5


def test_get_total_for_multiple_of_same_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("beans", 2)
    assert cart.total == 1.5


def test_get_total_for_item_by_kg():
    cart = ShoppingCart()
    cart.add_product("onions", 0.55)
    assert cart.total == 0.15


def test_get_total_for_multiple_items():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("butcombe")
    cart.add_product("coke")
    cart.add_product("onions", 1.2777)
    cart.add_product("beans")
    assert cart.total == 4.17


def test_raises_for_invalid_item():
    cart = ShoppingCart()
    with pytest.raises(InvalidProductException) as e:
        cart.add_product("tomacco")
    assert "Unexpected Item in Bagging Area" in e.value.args[0]


def test_raises_for_invalid_item_quantity():
    cart = ShoppingCart()
    with pytest.raises(ProductQuantityException) as e:
        cart.add_product("coke", 1.5)
    assert "Product quantity for coke must be specified in integers" in e.value.args[0]


def test_product_price_rounded_down_to_2_decimal_places():
    input_prices = [5.235, 0.999, 1.12214930, 1.1, 0.001]
    rounded_prices = [ShoppingCart._ShoppingCart__round_down_price(price) for price in input_prices]
    expected_prices = [5.23, 0.99, 1.12, 1.1, 0.01]
    assert rounded_prices == expected_prices
