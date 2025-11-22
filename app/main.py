from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.security import SecurityMiddleware
from app.routers import (
    root_router, health_router, agents_router, webhooks_telegram_router, 
    webhooks_stripe_router, webhooks_google_router, uploads_router, 
    users_router, modules_router, omoni_router, omoni_telegram_router,
    omoni_slack_router, omoni_connectors_router, agents_communicate_router
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("🚀 Donna API starting up...")
    
    yield
    
    logger.info("🛑 Donna API shutting down...")

app = FastAPI(
    title="Donna API",
    description="API principale pour l'architecture O'moni - Multi-service avec agents",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(SecurityMiddleware)

app.include_router(root_router, tags=["root"])
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(agents_router, prefix="/api/v1", tags=["agents"])
app.include_router(webhooks_telegram_router, prefix="/api/v1", tags=["webhooks"])
app.include_router(webhooks_stripe_router, prefix="/api/v1", tags=["webhooks"])
app.include_router(webhooks_google_router, prefix="/api/v1", tags=["webhooks"])
app.include_router(uploads_router, prefix="/api/v1", tags=["uploads"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(modules_router, prefix="/api/v1", tags=["modules"])
app.include_router(omoni_router, prefix="/api/v1", tags=["omoni"])
app.include_router(omoni_telegram_router, prefix="/api/v1/omoni", tags=["omoni-telegram"])
app.include_router(omoni_slack_router, prefix="/api/v1/omoni", tags=["omoni-slack"])
app.include_router(omoni_connectors_router, prefix="/api/v1/omoni", tags=["omoni-connectors"])
app.include_router(agents_communicate_router, prefix="/api/v1/agents", tags=["agents-communication"])

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )