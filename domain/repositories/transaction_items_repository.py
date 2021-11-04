from domain.db.config import session
from domain.entities.transaction_item import TransactionItem


def get_all_transaction_items(period_day=None):
    period_day_where = f"where t.period_name = '{period_day}'"

    if period_day not in [None, 'morning', 'afternoon', 'evening']:
        raise RuntimeError('Invalid period day')

    transactions = {}

    query = f"""
    select
        t.transaction_id,
        p.product_id
    from
        transactions t
    inner join
        transaction_items ti on
        ti.transaction_id = t.transaction_id
    inner join
        products p
        on p.product_id = ti.product_id
    {period_day_where if period_day else ""}
    group by t.transaction_id, p.product_id;
    """

    all = session.execute(query).all()

    for transaction in all:
        trans_id, prod_id = transaction

        if transactions.get(trans_id):
            transactions[trans_id] = transactions.get(
                trans_id).union([prod_id])
        else:
            transactions[trans_id] = set([prod_id])
    return transactions


def create_transaction_item(transaction_id: int, product_id: int):
    transaction_item = TransactionItem(transaction_id, product_id)
    session.add(transaction_item)
    return transaction_item
