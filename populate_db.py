import pandas

from domain.db.config import session
from domain.entities.product import Product
from domain.entities.transaction import Transaction
from domain.entities.transaction_item import TransactionItem
from domain.repositories.product_repository import (create_product,
                                                    get_product_by_name)
from domain.repositories.transaction_items_repository import \
    create_transaction_item
from domain.repositories.transaction_repository import create_transaction

df = pandas.read_csv('basket.csv', sep=',')


def cache_items():
    items = {}

    def find(name):
        if items.get(name):
            return items.get(name)

        item = get_product_by_name(name)

        items[name] = item
        return item

    return find


def populate_products(df):
    deduplicated = df['Item'].drop_duplicates()
    for product_name in deduplicated:
        create_product(product_name)


def populate_items(transaction, items):
    for item in items:
        item_db = items_cache(item)

        create_transaction_item(
            transaction.transaction_id, item_db.product_id)


def populate_transactions(df):
    deduplicated = df[['Transaction', 'date_time',
                       'period_day', 'weekday_weekend']].drop_duplicates()
    for x in deduplicated.iterrows():
        elem = x[1]
        transaction = create_transaction(
            elem.date_time, elem.period_day, elem.weekday_weekend)

        items = df[df['Transaction'] == elem.Transaction]['Item']
        populate_items(transaction, items)


items_cache = cache_items()

populate_products(df)
populate_transactions(df)

session.commit()
