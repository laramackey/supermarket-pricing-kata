from typing import Dict, Type, Union

import pytest
from supermarket_pricing.offers import ThreeForTwo, ThreeFromSetForPrice, TwoForPrice
from supermarket_pricing.product import Product


@pytest.fixture
def test_product_catalogue() -> Dict[str, Union[Product, Type[Product]]]:
    return {
        "a": Product("a", 1.0),
        "b": Product("b", 1.0),
        "c": Product("c", 1.1),
        "d": Product("d", 1.2),
    }


def test_singular_three_for_two_offer(test_product_catalogue):
    offer = ThreeForTwo(test_product_catalogue["a"])
    cart_count = {"a": 3}  # Price 1.0
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 3 * 1.0= 3.0
    # After Discount = 3.0 - 1.0 = 2.0
    assert discount_amount == 1.0


def test_multiple_three_for_two_offer(test_product_catalogue):
    offer = ThreeForTwo(test_product_catalogue["a"])
    cart_count = {"a": 7}  # Price 1.0
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 7 * 1.0= 7.0
    # After Discount = 7.0 - 2.0 = 5.0
    assert discount_amount == 2.0


def test_singular_two_for_price_offer(test_product_catalogue):
    offer = TwoForPrice(test_product_catalogue["b"], 1.5)
    cart_count = {"b": 2}  # Price 1.0
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 2 * 1.0 = 2.0
    # After Discount = 2.0 - 1.5 - 0.5
    assert discount_amount == 0.5


def test_multiple_two_for_price_offer(test_product_catalogue):
    offer = TwoForPrice(test_product_catalogue["b"], 1.5)
    cart_count = {"b": 5}  # Price 1.0
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 5 * 1.0 = 5.0
    # After Discount = 1.5 + 1.5 + 1.0 = 4.0
    assert discount_amount == 1.0


def test_singular_three_from_set_offer(test_product_catalogue):
    offer = ThreeFromSetForPrice(
        [test_product_catalogue["b"], test_product_catalogue["c"], test_product_catalogue["d"]], 3.0, "letters"
    )
    cart_count = {
        "b": 1,  # Price 1.0
        "c": 1,  # Price 1.1
        "d": 1,  # Price 1.2
    }
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 3.3
    # After Discount = 3.3 + 3.0 = 0.3
    assert discount_amount == 0.3


def test_multiple_three_from_set_offer(test_product_catalogue):
    offer = ThreeFromSetForPrice(
        [test_product_catalogue["b"], test_product_catalogue["c"], test_product_catalogue["d"]], 3.0, "letters"
    )
    cart_count = {
        "b": 1,  # Price 1.0
        "c": 3,  # Price 1.1
        "d": 3,  # Price 1.2
    }
    discount_amount = offer.check_and_apply(cart_count)
    # Before Discount = 3.6 + 3.3 + 1.0 = 7.9
    # After Discount = 6.0 + 1.2 = 7.2
    assert discount_amount == 0.7  # Only discounts 6 cheapest out of the 7
