from domain.db.config import session


def get_all_transaction_items():
    transactions = {}

    query = """
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
    group by t.transaction_id, p.product_id;
    """

    all = session.execute(query).all()

    for transaction in all:
        trans_id, prod_id = transaction

        if transactions.get(trans_id):
            transactions[trans_id] = transactions.get(trans_id).union([prod_id])
        else:
            transactions[trans_id] = set([prod_id])
    return transactions
