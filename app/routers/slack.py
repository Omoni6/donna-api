from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class SlackEvent(BaseModel):
    type: str = None
    challenge: str = None
    event: dict = None

@router.post("/events")
async def slack_events(event: SlackEvent):
    if event.type == "url_verification":
        return {"challenge": event.challenge}
    
    return {"status": "ok"}