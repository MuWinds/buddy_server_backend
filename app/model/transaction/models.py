from sqlalchemy import Column, Integer, String, Double, TIMESTAMP
from app.database.session import Base
from datetime import datetime


class Transactions(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "buddy"}
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Double, unique=True, nullable=False)
    remark = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, default=datetime.now())
