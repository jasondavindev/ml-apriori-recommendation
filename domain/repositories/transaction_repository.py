from datetime import datetime

from domain.db.config import session
from domain.entities.transaction import Transaction


def get_all_transactions() -> list[Transaction]:
    return session.query(Transaction).all()


def create_transaction(date_time, period_day, weekday_weekend) -> Transaction:
    transaction = Transaction(datetime.strptime(
        date_time, '%d-%m-%Y %H:%M'), period_day, weekday_weekend)
    session.add(transaction)
    session.commit()
    return transaction
