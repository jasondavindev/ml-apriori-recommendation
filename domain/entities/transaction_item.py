from domain.db.config import Base
from sqlalchemy import Column, Integer
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    transaction_item_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer(), ForeignKey(
        'transactions.transaction_id'), nullable=False)
    product_id = Column(Integer(), ForeignKey(
        'products.product_id'), nullable=False)

    product = relationship('Product', cascade='all,delete',
                           foreign_keys=[product_id])
    transaction = relationship(
        'Transaction', cascade='all,delete', foreign_keys=[transaction_id])

    def __init__(self, transaction_id, product_id):
        self.transaction_id = transaction_id
        self.product_id = product_id
