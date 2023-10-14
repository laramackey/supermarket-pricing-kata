from typing import List

from supermarket_pricing.receipt_printer import print_receipt
from supermarket_pricing.shopping_cart import AddedProduct, AppliedOffer


class StubCart:
    def __init__(
        self,
        products_in_cart: List[AddedProduct] = [],
        applied_offers: List[AppliedOffer] = [],
        sub_total=0.0,
        savings=0.0,
        total=0.0,
    ):
        self.products_in_cart = products_in_cart
        self.applied_offers = applied_offers
        self.sub_total = sub_total
        self.savings = savings
        self.total = total


def test_prints_receipt_for_items_priced_by_quantity(capsys):
    products_in_cart = [AddedProduct("green eggs", 2, 5.98, 0), AddedProduct("ham", 1, 4.5, 0)]
    cart = StubCart(products_in_cart=products_in_cart, total=10.48)
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Ham                  |  £4.50 |
| **Total to Pay**     | £10.48 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_items_priced_by_weight(capsys):
    products_in_cart = [
        AddedProduct("mushrooms", 0.567, 1.68, 2.97),
        AddedProduct("brussel sprouts", 0.232, 0.348, 1.5),
    ]
    cart = StubCart(products_in_cart=products_in_cart, total=2.03)
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.35 |
| **Total to Pay**     |  £2.03 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_mix_of_items_without_offers(capsys):
    products_in_cart = [
        AddedProduct("green eggs", 2, 5.98, 0),
        AddedProduct("mushrooms", 0.567, 1.68, 2.97),
        AddedProduct("brussel sprouts", 0.232, 0.348, 1.5),
        AddedProduct("ham", 1, 4.5, 0),
    ]
    cart = StubCart(products_in_cart=products_in_cart, total=12.51)
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.35 |
| Ham                  |  £4.50 |
| **Total to Pay**     | £12.51 |
"""
    assert captured.out == expected_output


def test_prints_receipt_for_mix_of_items_with_offers(capsys):
    products_in_cart = [
        AddedProduct("green eggs", 2, 5.98, 0),
        AddedProduct("mushrooms", 0.567, 1.68, 2.97),
        AddedProduct("brussel sprouts", 0.232, 0.348, 1.5),
        AddedProduct("ham", 1, 4.5, 0),
    ]
    applied_offers = [AppliedOffer("Green eggs 2 for 1", 2.99), AppliedOffer("Mushrooms 50p off", 0.5)]
    cart = StubCart(
        products_in_cart=products_in_cart, applied_offers=applied_offers, sub_total=12.51, savings=3.49, total=9.02
    )
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Green eggs x 2       |  £5.98 |
| Mushrooms            |        |
| 0.567 kg @ £2.97/kg  |  £1.68 |
| Brussel sprouts      |        |
| 0.232 kg @ £1.50/kg  |  £0.35 |
| Ham                  |  £4.50 |
| **Sub-total**        | £12.51 |
| **Savings**          |        |
| Green eggs 2 for 1   | -£2.99 |
| Mushrooms 50p off    | -£0.50 |
| **Total savings**    |  £3.49 |
| **Total to Pay**     |  £9.02 |
"""
    assert captured.out == expected_output
