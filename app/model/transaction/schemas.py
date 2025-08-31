from pydantic import BaseModel


class TransactionInfo(BaseModel):
    amount: float
    remark: str
