from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.model.users import schemas, service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/login", response_model=schemas.Token)
async def login(
    account: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await service.authenticate_user(db, account, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect account or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.Token)
async def register(
    account: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await service.create_user(db, account, password)
    access_token = service.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
