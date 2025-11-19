from fastapi import APIRouter

router = APIRouter()

@router.get("/v1")
async def health_check():
    return {"status": "ok", "api": "donna-api"}