from supermarket_pricing.receipt_printer import print_receipt
from supermarket_pricing.shopping_cart import AddedProduct


class StubCart:
    def __init__(self, products_in_cart):
        self.products_in_cart = products_in_cart


def test_prints_receipt_for_one_item(capsys):
    products_in_cart = [AddedProduct("green eggs", 2, 5.98), AddedProduct("ham", 1, 4.5)]
    cart = StubCart(products_in_cart)
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = "green eggs: 5.98\nham: 4.5\n"
    assert captured.out == expected_output
