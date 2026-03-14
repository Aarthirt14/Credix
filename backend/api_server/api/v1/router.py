from fastapi import APIRouter

from api_server.api.v1.endpoints import auth, customers, transactions, voice

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(voice.router, tags=["voice"])
api_router.include_router(transactions.router, tags=["transactions"])

