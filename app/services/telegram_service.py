import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Processing Telegram update: {update.get('update_id')}")
        
        if 'message' in update:
            message = update['message']
            self.logger.info(f"Message from {message.get('from', {}).get('id')}: {message.get('text', '')}")
        
        return {"status": "processed", "update_id": update.get('update_id')}
    
    async def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        self.logger.info(f"Sending message to chat {chat_id}: {text}")
        return {"status": "sent", "chat_id": chat_id, "text": text}