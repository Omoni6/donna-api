import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Processing Slack event: {event.get('type')}")
        
        if event.get('type') == 'url_verification':
            return {"challenge": event.get('challenge')}
        
        if 'event' in event:
            inner_event = event['event']
            if inner_event.get('type') == 'message':
                self.logger.info(f"Message from {inner_event.get('user')}: {inner_event.get('text', '')}")
        
        return {"status": "ok"}
    
    async def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        self.logger.info(f"Sending message to channel {channel}: {text}")
        return {"status": "sent", "channel": channel, "text": text}