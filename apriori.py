from domain.repositories.product_repository import get_all_products
from domain.repositories.transaction_items_repository import get_all_transaction_items
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--period-day', required=False)
parser.add_argument('--min-sup', required=True, type=float)
parser.add_argument('--min-conf', required=True, type=float)
args = parser.parse_args()

MIN_SUP = args.min_sup
MIN_CONF = args.min_conf
PERIOD_DAY = args.period_day


def prune(rules, min_sup, min_conf):
    return [rule for rule in rules if rule['support'] >= min_sup and rule['confidence'] >= min_conf]


def get_strongest_associations():
    associations = {}

    print("Retrieving transactions and products")
    transactions = get_all_transaction_items(period_day=PERIOD_DAY)
    products = get_all_products()
    max = len(products)

    support_list = []
    confidence_list = []

    print(f"Calculating support for {max} combinations")
    print("===================================")

    for product in products:
        support_value = support(
            product.product_id, product.product_id, transactions)

        support_list.append({
            "support": support_value,
            "confidence": 1,
            "rule": str(product.product_id),
            "product_name": product.product_name
        })

    sup_prune_list = prune(support_list, MIN_SUP, 1)

    for item1 in sup_prune_list:
        for item2 in sup_prune_list:
            if item1['rule'] != item2['rule']:
                rule = f"{item1['rule']}_{item2['rule']}"
                support_value = support(
                    int(item1['rule']), int(item2['rule']), transactions)
                confidence_value = confidence(
                    int(item1['rule']), int(item2['rule']), transactions)

                confidence_list.append({
                    "support": support_value,
                    "confidence": confidence_value,
                    "rule": rule,
                    "combination": f"{item1['product_name']} - {item2['product_name']}"
                })

    associations = prune(confidence_list, MIN_SUP, MIN_CONF)
    associations = sorted(associations,
                          key=lambda x: (x["confidence"], x['support']))

    return associations[-2:]


def count_frequence(transactions: dict[int, set[int]], itemset: set[int]):
    count = 0

    for items in transactions.values():
        if itemset.issubset(items):
            count += 1

    return count


def support(first_item: int, second_item: int, transactions: dict[int, set[int]]):
    """
    Returns the support of an itemset in a list of transactions.
    """

    itemset = set([first_item, second_item])
    return count_frequence(transactions, itemset) / len(transactions.keys())


def confidence(first_item: int, second_item: int, transactions: dict[int, set[int]]):
    """
    Returns the confidence of an itemset in a list of transactions.
    """
    itemset = set([first_item, second_item])

    count = 0

    for transaction_items in transactions.values():
        if first_item in transaction_items:
            count += 1

    return count_frequence(transactions, itemset) / count


def main():
    if __name__ == "__main__":
        strongest_associations = get_strongest_associations()
        print(strongest_associations)


main()
