from sqlalchemy.ext.asyncio import AsyncSession
from app.model.chat.models import AgentChat, AgentCharacter
from app.llm_model import openai
from sqlalchemy import select


async def create_character(
    db: AsyncSession, character: str, prompt: str
) -> AgentCharacter:
    character = AgentCharacter(name=character, prompt=prompt)
    db.add(character)
    await db.commit()
    await db.refresh(character)
    return character


async def get_character_prompt(
    db: AsyncSession, character: str
) -> AgentCharacter | None:
    stmt = select(AgentCharacter).where(AgentCharacter.name == character)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def create_chat_session(
    db: AsyncSession, user_id: int, character: str
) -> AgentChat:
    character_prompt = await get_character_prompt(db, character)
    sys_prompt = [{"role": "system", "content": character_prompt.prompt}]
    chat_session = AgentChat(
        user_id=user_id, character=character, chat_content=sys_prompt
    )
    db.add(chat_session)
    await db.commit()
    await db.refresh(chat_session)
    return chat_session


async def get_chat_session(db: AsyncSession, session_id: int) -> AgentChat | None:
    stmt = select(AgentChat).where(AgentChat.id == int(session_id))
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def update_chat_history(
    db: AsyncSession, chat_session: AgentChat, chat_history: list
) -> None:
    chat_session.chat_content = chat_history
    db.add(chat_session)
    await db.commit()
    await db.refresh(chat_session)


async def get_chat_response(db: AsyncSession, session_id: int, question: str) -> str:
    chat_session = await get_chat_session(db, session_id)
    if not chat_session:
        return False
    chat_history = list(chat_session.chat_content)
    chat_history.append({"role": "user", "content": question})
    response = openai.get_qwen_response(chat_history)
    chat_history.append({"role": "assistant", "content": response})
    await update_chat_history(db, chat_session, chat_history)
    return response


async def delete_chat_session(db: AsyncSession, user_id: int) -> None:
    chat_session = await get_chat_session(db, user_id)
    db.delete(chat_session)
    await db.commit()
