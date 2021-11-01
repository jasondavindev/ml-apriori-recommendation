from datetime import datetime

import pandas

from domain.db.config import session
from domain.entities.product import Product
from domain.entities.transaction import Transaction
from domain.entities.transaction_item import TransactionItem

df = pandas.read_csv('basket.csv', sep=',')


def cache_items(session):
    items = {}

    def find(name):
        if items.get(name):
            return items.get(name)

        item = session.query(Product).filter_by(
            product_name=name).first()

        items[name] = item
        return item

    return find


def populate_products(df, session):
    deduplicated = df['Item'].drop_duplicates()
    for product in deduplicated:
        prod = Product(product)
        session.add(prod)


def populate_items(session, transaction, items):
    for item in items:
        item_db = items_cache(item)

        transaction_item = TransactionItem(
            transaction.transaction_id, item_db.product_id)
        session.add(transaction_item)


def populate_transactions(df, session):
    deduplicated = df[['Transaction', 'date_time',
                       'period_day', 'weekday_weekend']].drop_duplicates()
    for x in deduplicated.iterrows():
        elem = x[1]
        transaction = Transaction(
            datetime.strptime(elem.date_time, '%d-%m-%Y %H:%M'), elem.period_day, elem.weekday_weekend)
        session.add(transaction)
        session.commit()

        items = df[df['Transaction'] == elem.Transaction]['Item']
        populate_items(session, transaction, items)


items_cache = cache_items(session)

populate_products(df, session)
populate_transactions(df, session)

session.commit()
