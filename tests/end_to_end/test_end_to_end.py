from supermarket_pricing.receipt_printer import print_receipt
from supermarket_pricing.shopping_cart import ShoppingCart


def test_supermarket_receipt_without_offers(capsys):
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("butcombe")
    cart.add_product("coke")
    cart.add_product("onions", "1.2777")
    cart.add_product("beans")
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Beans                |  £0.50 |
| Butcombe             |  £2.10 |
| Coke                 |  £0.70 |
| Onions               |        |
| 1.277 kg @ £0.29/kg  |  £0.37 |
| Beans                |  £0.50 |
| **Total to Pay**     |  £4.17 |
"""
    assert captured.out == expected_output


def test_supermarket_receipt_with_offers(capsys):
    cart = ShoppingCart()
    cart.add_product("beans")
    cart.add_product("beans")
    cart.add_product("beans")
    cart.add_product("coke")
    cart.add_product("coke")
    cart.add_product("oranges", "0.2")
    cart.add_product("arbor ale")
    cart.add_product("kaleidoscope")
    cart.add_product("kaleidoscope")
    cart.add_product("butcombe")
    print_receipt(cart)
    captured = capsys.readouterr()
    expected_output = """| Beans                |  £0.50 |
| Beans                |  £0.50 |
| Beans                |  £0.50 |
| Coke                 |  £0.70 |
| Coke                 |  £0.70 |
| Oranges              |        |
| 0.200 kg @ £1.99/kg  |  £0.39 |
| Arbor ale            |  £2.20 |
| Kaleidoscope         |  £2.50 |
| Kaleidoscope         |  £2.50 |
| Butcombe             |  £2.10 |
| **Sub-total**        | £12.59 |
| **Savings**          |        |
| Beans 3 for 2        | -£0.50 |
| Coke 2 for £1.00     | -£0.40 |
| Ales 3 for £6.00     | -£0.80 |
| **Total savings**    |  £1.70 |
| **Total to Pay**     | £10.89 |
"""
    assert captured.out == expected_output
