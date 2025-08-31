from sqlalchemy import Column, Integer, String, JSON
from app.database.session import Base


class AgentChat(Base):
    __tablename__ = "agent_chat"
    __table_args__ = {"schema": "buddy"}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    chat_content = Column(JSON, nullable=False)
    character = Column(String, nullable=False)


class AgentCharacter(Base):
    __tablename__ = "agent_character"
    __table_args__ = {"schema": "buddy"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
