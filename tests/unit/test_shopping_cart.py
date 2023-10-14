from decimal import Decimal

import pytest
from supermarket_pricing.exceptions import (
    InvalidProductException,
    ProductQuantityException,
)
from supermarket_pricing.product import Price
from supermarket_pricing.shopping_cart import ShoppingCart


def test_get_total_for_one_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    assert cart.sub_total == Price("0.5")
    assert cart.savings == Price("0")
    assert cart.total == Price("0.5")


def test_get_total_for_multiple_of_same_item():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("beans", "2")
    assert cart.sub_total == Price("1.5")
    assert cart.savings == Price("0.5")
    assert cart.total == Price("1")


def test_get_total_for_item_by_kg():
    cart = ShoppingCart()
    cart.add_product("onions", "0.55")
    assert cart.sub_total == Price("0.15")
    assert cart.savings == Price("0")
    assert cart.total == Price("0.15")


def test_get_total_for_multiple_items_without_offers():
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("butcombe")
    cart.add_product("coke")
    cart.add_product("onions", "1.2777")
    cart.add_product("beans")
    assert cart.sub_total == Price("4.17")
    assert cart.savings == Price("0")
    assert cart.total == Price("4.17")


def test_get_total_for_with_offers():
    cart = ShoppingCart()
    cart.add_product("beans")  # 0.5
    cart.add_product("beans")  # 0.5
    cart.add_product("butcombe")  # 2.1
    cart.add_product("coke")  # 0.7
    cart.add_product("beans")  # 0.5
    cart.add_product("beans")  # 0.5
    assert cart.sub_total == Price("4.8")
    assert cart.savings == Price("0.5")  # 3 for 2 beans
    assert cart.total == Price("4.3")


def test_raises_for_invalid_item():
    cart = ShoppingCart()
    with pytest.raises(InvalidProductException) as e:
        cart.add_product("tomacco")
    assert "Unexpected Item in Bagging Area" in e.value.args[0]


@pytest.mark.parametrize(
    "input_value, error",
    [
        ("1.5", "specified in integers"),
        ("0", "a positive value"),
        ("-8", "a positive value"),
        ("a million", "a valid number"),
    ],
)
def test_raises_for_invalid_item_quantity(input_value, error):
    cart = ShoppingCart()
    with pytest.raises(ProductQuantityException) as e:
        cart.add_product("coke", input_value)
    assert f"Product quantity for coke must be {error}" in e.value.args[0]


@pytest.mark.parametrize(
    "input_price, expected_price",
    [
        (Price("5.235"), Price("5.23")),
        (Price("0.999"), Price("0.99")),
        (Price("1.12214930"), Price("1.12")),
        (Price("1.1"), Price("1.10")),
        (Price("0.001"), Price("0.01")),
    ],
)
def test_product_price_rounded_down_to_2_decimal_places(input_price, expected_price):
    rounded_price = ShoppingCart._ShoppingCart__round_down_price(input_price)
    assert rounded_price == expected_price


@pytest.mark.parametrize(
    "input, expected",
    [
        (Decimal("5.235"), False),
        (Decimal("5.000000000001"), False),
        (Decimal("2.00000000"), True),
        (Decimal("3"), True),
    ],
)
def test_decimal_is_int(input, expected):
    is_int = ShoppingCart._ShoppingCart__decimal_is_int(input)
    assert is_int == expected
