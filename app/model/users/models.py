from sqlalchemy import Boolean, Column, Integer, String
from app.database.session import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "buddy"}
    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    agent_transaction_limit = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
