from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.agent import router as agent_router
from app.api.transactions import router as transactions_router

app = FastAPI(title="Buddy Backend")

app.include_router(users_router)
app.include_router(agent_router)
app.include_router(transactions_router)
