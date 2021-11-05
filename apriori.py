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


def count_frequence(transactions, itemset):
    count = 0

    for items in transactions.values():
        if itemset.issubset(items):
            count += 1

    return count


def support(first_item: int, second_item: int, transactions):
    """
    Returns the support of an itemset in a list of transactions.
    """

    itemset = set([first_item, second_item])
    return count_frequence(transactions, itemset) / len(transactions.keys())


def confidence(first_item: int, second_item: int, transactions):
    """
    Returns the confidence of an itemset in a list of transactions.
    """
    itemset = set([first_item, second_item])

    count = 0

    for transaction_items in transactions.values():
        if first_item in transaction_items:
            count += 1

    return count_frequence(transactions, itemset) / count

def get_rules_as_int_list(rules):
    rules_set = [(e['rule'].split('_')) for e in rules]
    return [set([int(x) for x in e]) for e in rules_set]

def transform_transactions_to_items_lists(transactions):
    return [list(e[1]) for e in transactions.items()]

def match_apyori_and_apriori(apyori_results, apriori_results):
    return [e for e in apyori_results if e.items.issubset(apriori_results[0]) or e.items.issubset(apriori_results[1])]

def main():
    if __name__ == "__main__":
        print("ALL TRANSACTIONS")
        all_transactions = transform_transactions_to_items_lists(get_all_transaction_items())
        
        strongest_associations = get_strongest_associations(MIN_SUP, MIN_CONF)
        rules_set = get_rules_as_int_list(strongest_associations)

        apyori_results = list(apriori(all_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF))
        apyori_results_match = match_apyori_and_apriori(apyori_results, rules_set)

        print(strongest_associations)
        print(apyori_results_match)

        print("MORNING TRANSACTIONS")
        morning_transactions = transform_transactions_to_items_lists(get_all_transaction_items('morning'))

        strongest_associations = get_strongest_associations(MIN_SUP, MIN_CONF, 'morning')
        rules_set = get_rules_as_int_list(strongest_associations)

        apyori_results = list(apriori(morning_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF))
        apyori_results_match = match_apyori_and_apriori(apyori_results, rules_set)

        print(strongest_associations)
        print(apyori_results_match)

        print("AFTERNOON TRANSACTIONS")
        afternoon_transactions = transform_transactions_to_items_lists(get_all_transaction_items('afternoon'))

        strongest_associations = get_strongest_associations(MIN_SUP, MIN_CONF, 'afternoon')
        rules_set = get_rules_as_int_list(strongest_associations)

        apyori_results = list(apriori(afternoon_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF))
        apyori_results_match = match_apyori_and_apriori(apyori_results, rules_set)

        print(strongest_associations)
        print(apyori_results_match)

        print("EVENING TRANSACTIONS")
        evening_transactions = transform_transactions_to_items_lists(get_all_transaction_items('evening'))

        strongest_associations = get_strongest_associations(MIN_SUP, MIN_CONF, 'evening')
        rules_set = get_rules_as_int_list(strongest_associations)

        apyori_results = list(apriori(evening_transactions, min_support=MIN_SUP, min_confidence=MIN_CONF))
        apyori_results_match = match_apyori_and_apriori(apyori_results, rules_set)

        print(strongest_associations)
        print(apyori_results_match)

        # LIFT PARAM
        # Lift basically tells us that the likelihood of buying a Burger and Ketchup
        # together is 3.33 times more than the likelihood of just buying the ketchup.
        # A Lift of 1 means there is no association between products A and B.
        # Lift of greater than 1 means products A and B are more likely to be bought together.

main()
