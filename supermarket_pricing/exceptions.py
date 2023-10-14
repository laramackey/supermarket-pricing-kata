class ShoppingCartException(Exception):
    pass


class ProductQuantityException(ShoppingCartException):
    pass


class InvalidProductException(ShoppingCartException):
    pass


class ProductException(Exception):
    pass
