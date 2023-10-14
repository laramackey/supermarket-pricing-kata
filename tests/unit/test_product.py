import pytest
from supermarket_pricing.exceptions import InvalidProductException
from supermarket_pricing.product import Price, Product, Weight


@pytest.mark.parametrize(
    "price, price_string",
    [
        (Price("5.235"), "£5.23"),
        (Price("0.999"), "£0.99"),
        (Price("1.12214930"), "£1.12"),
        (Price("1.1"), "£1.10"),
        (Price("111.001"), "£111.00"),
    ],
)
def test_price_class_prints_to_two_decimal_places(capsys, price, price_string):
    print(price)
    captured = capsys.readouterr()
    assert captured.out == price_string + "\n"


@pytest.mark.parametrize(
    "price, price_string",
    [
        (Weight("5.235"), "5.235"),
        (Weight("0.9999"), "0.999"),
        (Weight("1.12214930"), "1.122"),
        (Weight("1.1"), "1.100"),
        (Weight("111.0001"), "111.000"),
    ],
)
def test_weight_class_prints_to_three_decimal_places(capsys, price, price_string):
    print(price)
    captured = capsys.readouterr()
    assert captured.out == price_string + "\n"


def test_raises_product_with_invalid_price():
    with pytest.raises(InvalidProductException) as e:
        Product("foo", Price("0.333"))
    assert "Invalid product price 0.333: must not have more than 2 decimal places" in e.value.args[0]
