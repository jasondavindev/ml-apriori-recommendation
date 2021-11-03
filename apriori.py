from itertools import combinations, product

from domain.entities.product import Product
from domain.entities.transaction import Transaction
from domain.repositories.product_repository import get_all_products
from domain.repositories.transaction_repository import get_all_transactions


def get_strongest_associations():
    associations = {}

    transactions = get_all_transactions()
    products = get_all_products()

    combinations_of_products = list(combinations(products, 2))

    count = 0
    max = len(combinations_of_products)

    print(f"Calculating associations for {max} combinations")
    print("===================================")
    for combination in combinations_of_products:
        first_item = combination[0]
        second_item = combination[1]
        support_value = support(first_item, second_item, transactions)
        confidence_value = confidence(first_item, second_item, transactions)

        associations[(first_item.product_name, second_item.product_name)] = {
            "support": support_value,
            "confidence": confidence_value
        }

        print(
            f"combination: {first_item.product_name} - {second_item.product_name}")
        print(f"support: {support_value}")
        print(f"confidence: {confidence_value}")
        print(f"{count} / {max}")
        print("===================================")

        count += 1

    associations = sorted(associations.items(),
                          key=lambda x: x[1]["confidence"])
    return [associations.pop(), associations.pop()]


def support(first_item: Product, second_item: Product, transactions: list[Transaction]):
    """
    Returns the support of an itemset in a list of transactions.
    """

    itemset = set([first_item.product_id, second_item.product_id])
    return len(
        [
            1 for transaction in transactions if itemset.issubset(
                set([item.product_id for item in transaction.transaction_items])
            )
        ]
    ) / len(transactions)


def confidence(first_item: Product, second_item: Product, transactions: list[Transaction]):
    """
    Returns the confidence of an itemset in a list of transactions.
    """
    itemset = set([first_item.product_id, second_item.product_id])
    return len(
        [
            1 for transaction in transactions if itemset.issubset(
                set([item.product_id for item in transaction.transaction_items])
            )
        ]
    ) / len(
        [
            1 for transaction in transactions if first_item.product_id in
            [item.product_id for item in transaction.transaction_items]
        ]
    )


def get_transaction_product_ids(transactions: list[Transaction]):
    transaction_product_ids = []
    for transaction in transactions:
        transaction_product_ids.append(
            [item.product_id for item in transaction.transaction_items])
    return transaction_product_ids


def main():
    if __name__ == "__main__":
        strongest_associations = get_strongest_associations()
        print(strongest_associations)


main()
