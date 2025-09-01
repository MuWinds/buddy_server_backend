from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.model.users import service as User_Service
from app.model.users.models import User
from app.model.chat import service

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/create_chat_session")
async def create_chat_session(
    character: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(User_Service.get_current_user),
):
    await service.create_chat_session(db, current_user.id, character)
    return {"result": "success"}


@router.get("/chat")
async def get_chat_response(
    user_prompt: str,
    session_id: str,
    current_user: User = Depends(User_Service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_limit = dict(current_user.limit)
    if current_user is None or user_limit["agent"] <= 0:
        return {
            "success": False,
            "response": "User not permission",
            "exception_reason": "User limit exceeded or User does not exist",
        }
    answer = await service.chat_request(db, session_id, question=user_prompt)
    user_limit["agent"] -= 1
    await User_Service.update_user_limit(db, current_user, user_limit)
    response = {"success": True, "response": answer}
    return response
