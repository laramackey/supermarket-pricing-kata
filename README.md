# Supermarket Pricing Calculator

## Requirements

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

### Pre-requrisites

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

I approached this coding exercise by applying Test-Driven Development principles. I initiated the process by addressing the simplest scenario, which was having a cart with a single item. Then, I gradually introduced more complexity to the code, maintaining a clear sense of progress. The optimization phase came after implementing the primary requirements, enhancing the readability and robustness of the code. You can review the specific steps and decisions in the pull requests I created. I introduced simple CI/CD early to ensure only linted and passing code made it's way on the main branch, and it also gave me a good level of confidence when refactoring that I had maintained the desired behaviour.

### Design Choices

Several key design choices informed the development of this solution:

-   Separation of concerns
    -   I kept `Offer`s and `Product`s as distinct objects. This choice offers more flexibility when adding or removing offers and allows for the application of discounts across multiple products. At first I considered associating offers directly with products for simplicity but would not fit the requirement for discounts across products. This approach would also require modifying a product each time a discount changes, which could become cumbersome if discounts are frequently change.
    -   Another example fo seperation of concerns is with the `ShoppingCart` and `print_receipt`. `print_receipt` is only resposible for formatting and printing items in the cart, whereas the `ShoppingCart` is responsibly for storing the items in the cart and calculating the total.
-   The `add_product` method increments product_quantities each time a product is added. I considered calculating product quantities only when getting the savings, as this is the only time it's needed and would be more memory efficient. However, this would have increased the time complexity to O(n) instead of the efficient O(1).
-   I used abstract classes for offers to guarantee a consistent structure and behavior across different types of offers.
-   Using data classes for products enables handling tasks like price validation and provides an inheritance structure for different product types.
-   `ShoppingCart` is a class as it is responsible for managing the state of the cart, which includes storing product information. I've used a property method to provide simple access to cart-related information.
-   `print_receipt` is just a function. This is to keeps things simple, as there is no need to store additional information for receipt generation.
-   After completing the main task, I made the decision to switch from using floats to using Decimals for price calculations. This transition was driven by the need for precision in financial applications. While it introduced some complexity, such as converting all values to decimal to perform arithmetic operations, and is less performant, it addressed issues related to float-based rounding errors (example below). It also removed rounding and string formatting in multiple places which is error prone.

```
>>> float(10.0-9.2)
0.8000000000000007
```

### Future improvements

-   **Handling Invalid Items**: The current implementation raises an error when an invalid item is scanned. In practice, it might be more user-friendly not to halt the program but rather add invalid items to a list. You could use a logging library to generate warnings about invalid items, allowing supermarket workers to take corrective action and remove the invalid item. You could add a check for the invalid_items list to be empty before you can checkout. EG:

```
if product := self.product_catalogue.get(product_name):
    ...
else:
    logger.warn(f"Invalid item scanned {product_name}: {quantity}")
    invalid_products.append((product_name, quantity))
```

-   **Removing Items**: Implementing the ability to remove items would be needed for a functional checkout software. This could involve adding a `remove_item(item_name, quantity)` method to decrement the count in `product_quantities.` It would also require adjusting the total property to include calculations for removed items and savings.

-   **Payment and Change Calculation**: Currently, the receipt does not show the payment or change. This could be improved by adding a `pay(amount)` method and calculating change as `abs(self.total - self.paid)` after validating that the customer has paid enough.

-   **Scalability**: In a more real-lift scenario where there would be 1000s of items and offers, you would retrieve items and offers via an API. A relational database on the backend could be used to fetch offers specific to the items in the cart, optimizing performance by eliminating the need to iterate through all available offers.

-   **User Experience** - You could consider checking for offers immediately after each item is scanned. This might provide immediate validation to the customer that the discount worked. However, this approach would come at the cost of additional complexity in terms of keeping track of applied discounts and removing them if items are removed from the cart.
