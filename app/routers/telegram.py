from fastapi import APIRouter

router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(payload: dict):
    return {"received": True}