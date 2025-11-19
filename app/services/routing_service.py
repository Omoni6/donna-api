import logging
from typing import Dict, Any, Optional
from ..services.telegram_service import TelegramService
from ..services.slack_service import SlackService

logger = logging.getLogger(__name__)

class RoutingService:
    def __init__(self):
        self.telegram_service = TelegramService()
        self.slack_service = SlackService()
        self.logger = logging.getLogger(__name__)
    
    async def route_webhook(self, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Routing webhook for service: {service}")
        
        if service == "telegram":
            return await self.telegram_service.process_update(payload)
        elif service == "slack":
            return await self.slack_service.process_event(payload)
        else:
            self.logger.warning(f"Unknown service: {service}")
            return {"error": f"Unknown service: {service}"}