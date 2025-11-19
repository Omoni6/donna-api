from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def events_health():
    return {"status": "ok", "service": "events"}