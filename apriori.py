import argparse

from apyori import apriori

from domain.repositories.product_repository import get_all_products
from domain.repositories.transaction_items_repository import \
    get_all_transaction_items

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


def get_strongest_associations(min_sup, min_conf, period_day=None):
    associations = {}

    transactions = get_all_transaction_items(period_day=period_day)
    products = get_all_products()

    support_list = []
    confidence_list = []

    for product in products:
        support_value = support(
            product.product_id, product.product_id, transactions)

        support_list.append({
            "support": support_value,
            "confidence": 1,
            "rule": str(product.product_id),
            "product_name": product.product_name
        })

    sup_prune_list = prune(support_list, min_sup, 1)

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

    associations = prune(confidence_list, min_sup, min_conf)
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
        print("ALL TRANSACTIONS")
        strongest_associations = get_strongest_associations(MIN_SUP, MIN_CONF)
        print(strongest_associations)

        print("MORNING TRANSACTIONS")
        strongest_associations_morning = get_strongest_associations(
            MIN_SUP, MIN_CONF, 'morning')
        print(strongest_associations_morning)

        print("AFTERNOON TRANSACTIONS")
        strongest_associations_afternoon = get_strongest_associations(
            MIN_SUP, MIN_CONF, 'afternoon')
        print(strongest_associations_afternoon)

        print("EVENING TRANSACTIONS")
        strongest_associations_evening = get_strongest_associations(
            MIN_SUP, MIN_CONF, 'evening')
        print(strongest_associations_evening)

        all_transactions = [list(e[1]) for e in get_all_transaction_items().items()]
        morning_transactions = [list(e[1]) for e in get_all_transaction_items('morning').items()]
        afternoon_transactions = [list(e[1]) for e in get_all_transaction_items('afternoon').items()]
        evening_transactions = [list(e[1]) for e in get_all_transaction_items('evening').items()]

        print('ALL TRANSACTIONS')
        print(list(apriori(all_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF)))
        print('MORNING TRANSACTIONS')
        print(list(apriori(morning_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF)))
        print('AFTERNOON TRANSACTIONS')
        print(list(apriori(afternoon_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF)))
        print('EVENING TRANSACTIONS')
        print(list(apriori(evening_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF)))

        # LIFT PARAM
        # Lift basically tells us that the likelihood of buying a Burger and Ketchup
        # together is 3.33 times more than the likelihood of just buying the ketchup.
        # A Lift of 1 means there is no association between products A and B.
        # Lift of greater than 1 means products A and B are more likely to be bought together.

main()
