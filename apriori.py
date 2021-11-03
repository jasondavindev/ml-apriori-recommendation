from itertools import combinations

from domain.entities.product import Product
from domain.repositories.product_repository import get_all_products
from domain.repositories.transaction_items_repository import get_all_transaction_items
from domain.repositories.transaction_repository import get_all_transactions

frequences = {}


def parse_transaction_items_to_dict(transactions):
    transactions_dict = {}

    for transaction in transactions:
        transactions_dict[transaction.transaction_id] = set(
            [item.product_id for item in transaction.transaction_items])

    return transactions_dict


def get_strongest_associations():
    associations = {}

    print("Retrieving transactions and products")
    transactions = get_all_transaction_items()
    products = get_all_products()

    print("Generating combinations")
    combinations_of_products = list(combinations(products, 2))

    count = 0
    max = len(combinations_of_products)

    print(f"Calculating associations for {max} combinations")
    print("===================================")
    for combination in combinations_of_products:
        first_item, second_item = combination
        support_value = support(first_item, second_item, transactions)
        confidence_value = confidence(
            first_item, second_item, transactions)

        associations[(first_item.product_name, second_item.product_name)] = {
            "support": support_value,
            "confidence": confidence_value
        }

        count += 1

        print(
            f"combination: {first_item.product_name} - {second_item.product_name}")
        print(f"support: {support_value}")
        print(f"confidence: {confidence_value}")
        print(f"{count} / {max}")
        print("===================================")

    associations = sorted(associations.items(),
                          key=lambda x: x[1]["confidence"])
    return [associations.pop(), associations.pop()]


def parse_items_to_key(items):
    return '_'.join([str(item) for item in items])


def count_frequence(transactions: dict[int, set[int]], itemset: set[int]):
    key = parse_items_to_key(itemset)

    if frequences.get(key):
        return frequences.get(key)

    count = 0

    for items in transactions.values():
        if itemset.issubset(items):
            count += 1

    frequences[key] = count

    return count


def support(first_item: Product, second_item: Product, transactions: dict[int, set[int]]):
    """
    Returns the support of an itemset in a list of transactions.
    """

    itemset = set([first_item.product_id, second_item.product_id])
    return count_frequence(transactions, itemset) / len(transactions.keys())


def confidence(first_item: Product, second_item: Product, transactions: dict[int, set[int]]):
    """
    Returns the confidence of an itemset in a list of transactions.
    """
    itemset = set([first_item.product_id, second_item.product_id])

    count = 0

    for transaction_items in transactions.values():
        if first_item.product_id in transaction_items:
            count += 1

    return count_frequence(transactions, itemset) / count


def main():
    if __name__ == "__main__":
        strongest_associations = get_strongest_associations()
        print(strongest_associations)


main()
