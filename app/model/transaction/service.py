from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.model.transaction.models import Transactions

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_transaction(
    db: AsyncSession, amount: str, remark: str, user_id: int
) -> Transactions:
    transacation = Transactions(amount=amount, remark=remark, user_id=user_id)
    db.add(transacation)
    await db.commit()
    await db.refresh(transacation)
    return transacation


# 根据用户ID列出交易记录
async def get_transaction_by_id(db: AsyncSession, user_id: int) -> Transactions | None:
    stmt = select(Transactions).where(Transactions.user_id == user_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def edit_transaction(
    db: AsyncSession, amount: str, remark: str, transaction_id: int
) -> Transactions:
    transaction = await get_transaction_by_id(db, transaction_id)
    transaction.amount = amount
    transaction.remark = remark
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def delete_transaction(db: AsyncSession, transaction_id: int) -> None:
    transaction = await get_transaction_by_id(db, transaction_id)
    db.delete(transaction)
    await db.commit()
    return
