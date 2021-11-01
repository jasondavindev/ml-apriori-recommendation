from domain.db.config import Base
from sqlalchemy import Column, DateTime, Integer, String


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime(), nullable=False)
    period_name = Column(String(length=255), nullable=False)
    weekday_end = Column(String(length=255), nullable=False)

    def __init__(self, date_time, period_name, weekday_end):
        self.date_time = date_time
        self.period_name = period_name
        self.weekday_end = weekday_end
