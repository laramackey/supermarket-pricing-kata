from decimal import Decimal
from typing import List

from supermarket_pricing.product import Price, Weight
from supermarket_pricing.receipt_printer import print_receipt
from supermarket_pricing.shopping_cart import AddedProduct, AppliedOffer


class StubCart:
    def __init__(
        self,
        products_in_cart: List[AddedProduct] = [],
        applied_offers: List[AppliedOffer] = [],
        sub_total: Price = Price("0"),
        savings: Price = Price("0"),
        total: Price = Price("0"),
    ):
        self.products_in_cart = products_in_cart
        self.applied_offers = applied_offers
        self.sub_total = sub_total
        self.savings = savings
        self.total = total


def test_prints_receipt_for_items_priced_by_quantity(capsys):
    products_in_cart = [
        AddedProduct("green eggs", Decimal("2"), Price("5.98"), Decimal("0")),
        AddedProduct("ham", Decimal("1"), Price("4.5"), Decimal("0")),
    ]
    cart = StubCart(products_in_cart=products_in_cart, total=Price("10.48"))
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Ham                  |  £4.50 |
| **Total to Pay**     | £10.48 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_items_priced_by_weight(capsys):
    products_in_cart = [
        AddedProduct("mushrooms", Weight("0.567"), Price("1.68"), Price("2.97")),
        AddedProduct("brussel sprouts", Weight("0.232"), Price("0.348"), Price("1.5")),
    ]
    cart = StubCart(products_in_cart=products_in_cart, total=Price("2.03"))
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.34 |
| **Total to Pay**     |  £2.03 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_mix_of_items_without_offers(capsys):
    products_in_cart = [
        AddedProduct("green eggs", Decimal("2"), Price("5.98"), Price("0")),
        AddedProduct("mushrooms", Weight("0.567"), Price("1.68"), Price("2.97")),
        AddedProduct("brussel sprouts", Weight("0.232"), Price("0.348"), Price("1.5")),
        AddedProduct("ham", Decimal("1"), Price("4.5"), Price("0")),
    ]
    cart = StubCart(products_in_cart=products_in_cart, total=Price("12.51"))
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.34 |
| Ham                  |  £4.50 |
| **Total to Pay**     | £12.51 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_mix_of_items_with_offers(capsys):
    products_in_cart = [
        AddedProduct("green eggs", Decimal("2"), Price("5.98"), Price("0")),
        AddedProduct("mushrooms", Weight("0.567"), Price("1.68"), Price("2.97")),
        AddedProduct("brussel sprouts", Weight("0.232"), Price("0.348"), Price("1.5")),
        AddedProduct("ham", Decimal("1"), Price(" 4.5"), Price("0")),
    ]
    applied_offers = [
        AppliedOffer("Green eggs 2 for 1", Price("2.99")),
        AppliedOffer("Mushrooms 50p off", Price("0.5")),
    ]
    cart = StubCart(
        products_in_cart=products_in_cart,
        applied_offers=applied_offers,
        sub_total=Price("12.51"),
        savings=Price("3.49"),
        total=Price("9.02"),
    )
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.34 |
| Ham                  |  £4.50 |
| **Sub-total**        | £12.51 |
| **Savings**          |        |
| Green eggs 2 for 1   | -£2.99 |
| Mushrooms 50p off    | -£0.50 |
| **Total savings**    |  £3.49 |
| **Total to Pay**     |  £9.02 |
"""
    assert captured.out == expected_output
