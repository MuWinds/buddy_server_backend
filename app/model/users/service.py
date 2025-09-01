from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.database.session import get_db
from app.core.config import settings
from app.model.users.models import User

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")  # 登录接口地址


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)


async def authenticate_user(
    db: AsyncSession, account: str, password: str
) -> User | None:
    from sqlalchemy import select

    res = await db.execute(select(User).where(User.account == account))
    user = res.scalar_one_or_none()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


async def create_user(db: AsyncSession, account: str, password: str) -> User:
    user = User(
        account=account,
        hashed_password=hash_password(password),
        limit={"transaction": 1000, "agent": 1000},
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 从数据库取用户
    user = await get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user


async def update_user_limit(db: AsyncSession, user: User, limit: dict) -> None:
    user.limit = limit
    db.add(user)
    await db.commit()
    await db.refresh(user)
