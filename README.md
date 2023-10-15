# Supermarket Pricing Calculator

## Functional Requirements

Write a program which works out how to price a shopping basket, allowing for different pricing structures including:

-   Three tins of beans for the price of two
-   Onions for 29p / kg
-   Two cans of coca-cola for £1
-   Any 3 ales from the set {…} for £6

Here’s an example of a receipt illustrating the type of output that should be possible

|                     |       |
| ------------------- | ----- |
| Beans               | 0.50  |
| Beans               | 0.50  |
| Beans               | 0.50  |
| Coke                | 0.70  |
| Coke                | 0.70  |
| Oranges             |       |
| 0.200 kg @ £1.99/kg | 0.40  |
| **Sub-total**       | 3.30  |
| **Savings**         |       |
| Beans 3 for 2       | -0.50 |
| Coke 2 for £1       | -0.40 |
| **Total savings**   | -0.90 |
| **Total to Pay**    | 2.40  |

## Instructions

### Pre-requisites

1. Install **Python 3.10.13**

Python versions can be managed easily on your machine with [pyenv](https://github.com/pyenv/pyenv)

2. Create a Virtual Environment

```
python3 -m venv .venv
. .venv/bin/activate
```

3. Download python dependencies

```
make setup
```

### Running tests

```
make test
```

## Discussion

### Process

-   I approached this exercise by applying Test-Driven Development principles. I started with the simplest scenario, having a cart with a single item. Then, I gradually introduced the other features such as adding items by weight and offers. After implementing the primary requirements, I worked on improving the readability and robustness of the code. You can review the specific steps in the closed pull requests.
-   I introduced simple CI/CD early to ensure only linted and passing code made it to the main branch, and to provide confidence when refactoring that I had maintained the desired behaviour.

### Design Choices

-   Separation of concerns
    -   I kept `Offer`s and `Product`s as distinct objects. This increases flexibility when adding or removing offers and allows for multi-product offers. At first I considered associating offers directly with products for simplicity, but this would not allow for an offer to be eligible across multiple products. This approach would also require modifying a product each time a offer changes, which could become cumbersome if offers are frequently changed.
    -   The `ShoppingCart` and `print_receipt` seperates the tasks of calculating totals and the formatting of receipts.
-   I used abstract classes for `Offer`s to guarantee a consistent structure and behavior across different types of offers.
-   I used data classes for `Product`s to handle tasks like price validation and provides an inheritance structure for different product types.
-   `ShoppingCart` is implemented as a class as it is responsible for managing the state of the cart and performing calculations. `@property` methods are used to provide simple access to cart-related information.
-   The `ShoppingCart.add_product` method increments `product_quantities` each time a product is added. I considered calculating `product_quantites` only when getting the savings, as this is the only time it's needed and would be more memory efficient. However, this would have increased the time complexity to O(n) instead of O(1).
-   `print_receipt`is implemented as a function for simplicity, as it is only responsible for printing the receipt and not storing information.
-   After completing the main task, I switched from using `float`s to `Decimal`s for price calculations. This introduced some complexity, such as converting all values to `Decimal` to perform arithmetic operations, and is less performant. However, it addresses issues related to float imprecision errors (example below) which could have severe consequences in financial applications. It also removed the need to repeat rounding and string formatting in multiple places in the code, which is error prone.

```
>>> 10.0-9.2
0.8000000000000007
```

```
>>> Decimal("10") - Decimal("9.2")
Decimal('0.8')
```

### Future improvements

-   **Handling Invalid Items**: The current implementation raises an error when an invalid item is scanned, which is not user-friendly. Instead you could add invalid items to a list and use a logging library to generate warnings about invalid items. This would allow supermarket workers to take corrective action and remove the invalid item. You could add a check that `invalid_items` is empty before you can checkout. EG:

```
if product := self.product_catalogue.get(product_name):
    ...
else:
    logger.warn(f"Invalid item scanned {product_name}: {quantity}")
    self.invalid_products.append((product_name, quantity))
```

-   **Removing Items**: This could involve adding a `remove_item(item_name, quantity)` method to decrement the count in `product_quantities`, and subtracting the cost of removed items when caclulation the total.

-   **Payment and Change Calculation**: This could be added by implementing `pay(amount)` method and calculating change as `abs(self.total - self.paid)` after validating that the customer has paid enough.

-   **Scalability**: In a more realistic scenario where there would be 1000s of items and offers, you would retrieve items and offers via an API. A relational database on the backend could be used to fetch offers specific to the items in the cart, optimizing performance by eliminating the need to iterate through all available offers.

-   **User Experience** - You could consider checking for offers after each item is scanned. This would provide immediate validation to the customer that the offer worked. However, this would come at the cost of additional complexity in terms of keeping track of applied offers and removing them if items are removed from the cart.
