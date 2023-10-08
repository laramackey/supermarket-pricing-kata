class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


product_catalogue = {
    "beans": Product("beans", 0.5),
    "coke": Product("coke", 0.7),
}
