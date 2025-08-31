from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.model.transaction import schemas, service
from app.model.users import service as User_Service
from app.model.users.models import User

router = APIRouter(prefix="/api/transaction", tags=["transaction"])


@router.post("/add_transaction")
async def add_transaction(
    form: schemas.TransactionInfo,
    current_user: User = Depends(User_Service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await service.create_transaction(db, form.amount, form.remark, current_user.id)
    return {"result": "success"}


@router.post("/edit_transaction")
async def edit_transaction(
    form: schemas.TransactionInfo,
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    transaction = await service.edit_transaction(
        db, form.amount, form.remark, transaction_id
    )
    return transaction


@router.post("/delete_transaction")
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    await service.delete_transaction(db, transaction_id)
    return {"result": "success"}


@router.get("/get_transaction")
async def get_transaction(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(User_Service.get_current_user),
):
    transaction = await service.get_transaction_by_id(db, current_user.id)
    return transaction
