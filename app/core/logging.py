import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """Formateur JSON pour les logs structurés"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Ajouter les données supplémentaires
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, "tenant_id"):
            log_entry["tenant_id"] = record.tenant_id
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

def setup_logging():
    """Configure le logging JSON structuré"""
    
    # Créer le dossier de logs
    log_dir = Path("/app/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configuration du logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = JSONFormatter()
    console_handler.setFormatter(console_formatter)
    
    # Handler pour le fichier
    file_handler = logging.FileHandler(log_dir / "donna-api.json")
    file_handler.setLevel(logging.INFO)
    file_formatter = JSONFormatter()
    file_handler.setFormatter(file_formatter)
    
    # Handler pour les erreurs
    error_handler = logging.FileHandler(log_dir / "errors.json")
    error_handler.setLevel(logging.ERROR)
    error_formatter = JSONFormatter()
    error_handler.setFormatter(error_formatter)
    
    # Ajouter les handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    # Configuration spécifique pour uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = [console_handler]
    
    logging.getLogger("app").info("📝 Logging configuré avec format JSON")

def get_logger(name: str) -> logging.Logger:
    """Récupère un logger configuré"""
    return logging.getLogger(f"app.{name}")

class RequestLoggingMiddleware:
    """Middleware pour logger les requêtes HTTP"""
    
    def __init__(self):
        self.logger = get_logger("requests")
    
    async def __call__(self, request, call_next):
        start_time = datetime.utcnow()
        
        # Log de la requête
        self.logger.info(
            "Request started",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else None,
                "headers": dict(request.headers)
            }
        )
        
        response = await call_next(request)
        
        # Log de la réponse
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        self.logger.info(
            "Request completed",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration": duration,
                "client": request.client.host if request.client else None
            }
        )
        
        return response