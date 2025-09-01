from sqlalchemy import Boolean, Column, Integer, String, JSON
from app.database.session import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "buddy"}
    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    limit = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
