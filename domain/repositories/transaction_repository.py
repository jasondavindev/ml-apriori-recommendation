from domain.db.config import session
from domain.entities.transaction import Transaction


def get_all_transactions() -> list[Transaction]:
    return session.query(Transaction).all()
