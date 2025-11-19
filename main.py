from fastapi import FastAPI
from app.routers import root, telegram, slack, events

app = FastAPI(
    title="Donna API",
    description="API pour la gestion des webhooks Telegram et Slack",
    version="1.0.0"
)

app.include_router(root.router)
app.include_router(telegram.router, prefix="/api/v1/telegram", tags=["telegram"])
app.include_router(slack.router, prefix="/api/v1/slack", tags=["slack"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])