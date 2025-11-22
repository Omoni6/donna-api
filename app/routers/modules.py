from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional, List
import logging
import psutil
import platform
from datetime import datetime
from ..core.security import get_tenant_id
from ..core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/modules", tags=["modules"])

def get_system_info() -> Dict[str, Any]:
    """Obtenir les informations système"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Mémoire
        memory = psutil.virtual_memory()
        
        # Disque
        disk = psutil.disk_usage('/')
        
        # Réseau
        network = psutil.net_io_counters()
        
        # Processus
        processes = len(psutil.pids())
        
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            "processes": processes
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des infos système: {e}")
        return {"error": str(e)}

@router.get("/status")
async def get_modules_status(tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Obtenir le statut de tous les modules du système"""
    try:
        system_info = get_system_info()
        
        modules_status = {
            "api": {
                "status": "healthy",
                "version": "1.0.0",
                "uptime": "N/A",
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "donna_worker": {
                "status": "unknown",
                "url": settings.DONNA_WORKER_URL,
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "telegram": {
                "status": "configured",
                "webhook_url": "/api/v1/webhooks/telegram",
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "stripe": {
                "status": "configured", 
                "webhook_url": "/api/v1/webhooks/stripe",
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "google": {
                "status": "configured",
                "webhooks": {
                    "calendar": "/api/v1/webhooks/google/calendar",
                    "gmail": "/api/v1/webhooks/google/gmail", 
                    "drive": "/api/v1/webhooks/google/drive"
                },
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "database": {
                "status": "simulated",
                "type": "mock",
                "last_check": datetime.utcnow().isoformat() + "Z"
            },
            "file_storage": {
                "status": "active",
                "upload_directory": "uploads/",
                "max_file_size": "10MB",
                "last_check": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Ajouter les infos système
        modules_status["system"] = {
            "status": "healthy" if system_info.get("cpu", {}).get("percent", 100) < 90 else "warning",
            "info": system_info,
            "last_check": datetime.utcnow().isoformat() + "Z"
        }
        
        logger.info(
            "Statut des modules récupéré",
            extra={
                "tenant_id": tenant_id,
                "modules_count": len(modules_status),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "modules": modules_status,
            "overall_status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération du statut des modules: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur statut modules: {str(e)}")

@router.get("/health/{module_name}")
async def get_module_health(module_name: str, tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Obtenir la santé d'un module spécifique"""
    try:
        module_name = module_name.lower()
        
        health_checks = {
            "api": lambda: {"status": "healthy", "version": "1.0.0"},
            "system": lambda: {"status": "healthy" if get_system_info().get("cpu", {}).get("percent", 100) < 90 else "warning", "info": get_system_info()},
            "donna_worker": lambda: {"status": "unknown", "message": "Requires external check"},
            "telegram": lambda: {"status": "configured", "webhook_active": True},
            "stripe": lambda: {"status": "configured", "webhook_active": True},
            "google": lambda: {"status": "configured", "webhooks_count": 3},
            "database": lambda: {"status": "simulated", "type": "mock"},
            "file_storage": lambda: {"status": "active", "directory": "uploads/"}
        }
        
        if module_name not in health_checks:
            raise HTTPException(status_code=404, detail=f"Module {module_name} non trouvé")
        
        health_info = health_checks[module_name]()
        
        logger.info(
            f"Santé du module {module_name} récupérée",
            extra={
                "module": module_name,
                "status": health_info.get("status"),
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "module": module_name,
            "health": health_info,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération de la santé du module {module_name}: {str(e)}",
            extra={
                "module": module_name,
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur santé module: {str(e)}")

@router.post("/restart/{module_name}")
async def restart_module(module_name: str, tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Redémarrer un module spécifique"""
    try:
        module_name = module_name.lower()
        
        # Modules qui peuvent être "redémarrés"
        restartable_modules = ["telegram", "stripe", "google", "file_storage"]
        
        if module_name not in restartable_modules:
            raise HTTPException(status_code=400, detail=f"Module {module_name} non redémarrable")
        
        # Simuler le redémarrage
        logger.info(
            f"Redémarrage du module {module_name}",
            extra={
                "module": module_name,
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "message": f"Module {module_name} redémarré avec succès",
            "module": module_name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors du redémarrage du module {module_name}: {str(e)}",
            extra={
                "module": module_name,
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur redémarrage: {str(e)}")

@router.get("/metrics")
async def get_system_metrics(tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Obtenir les métriques système détaillées"""
    try:
        system_info = get_system_info()
        
        # Calculer des métriques supplémentaires
        metrics = {
            "cpu_usage_history": [psutil.cpu_percent(interval=0.1) for _ in range(10)],
            "memory_usage_trend": {
                "used_gb": system_info["memory"]["used"] / (1024**3),
                "available_gb": system_info["memory"]["available"] / (1024**3),
                "total_gb": system_info["memory"]["total"] / (1024**3)
            },
            "disk_usage": {
                "used_gb": system_info["disk"]["used"] / (1024**3),
                "free_gb": system_info["disk"]["free"] / (1024**3),
                "total_gb": system_info["disk"]["total"] / (1024**3),
                "percent": system_info["disk"]["percent"]
            },
            "network_activity": {
                "mb_sent": system_info["network"]["bytes_sent"] / (1024**2),
                "mb_received": system_info["network"]["bytes_recv"] / (1024**2)
            },
            "process_count": system_info["processes"]
        }
        
        logger.info(
            "Métriques système récupérées",
            extra={
                "tenant_id": tenant_id,
                "cpu_percent": system_info.get("cpu", {}).get("percent"),
                "memory_percent": system_info.get("memory", {}).get("percent"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "metrics": metrics,
            "system_info": system_info,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération des métriques: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur métriques: {str(e)}")

@router.get("/dependencies")
async def get_module_dependencies(tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Obtenir les dépendances entre modules"""
    try:
        dependencies = {
            "api": {
                "depends_on": ["system"],
                "required_by": ["telegram", "stripe", "google", "users", "uploads"],
                "external_dependencies": ["fastapi", "uvicorn", "pydantic"]
            },
            "donna_worker": {
                "depends_on": ["api"],
                "required_by": ["agents"],
                "external_dependencies": ["httpx"]
            },
            "telegram": {
                "depends_on": ["api"],
                "required_by": [],
                "external_dependencies": ["python-telegram-bot"]
            },
            "stripe": {
                "depends_on": ["api"],
                "required_by": [],
                "external_dependencies": ["stripe-python"]
            },
            "google": {
                "depends_on": ["api"],
                "required_by": [],
                "external_dependencies": ["google-api-python-client"]
            },
            "database": {
                "depends_on": ["system"],
                "required_by": ["users", "analytics"],
                "external_dependencies": ["sqlalchemy", "alembic"]
            },
            "file_storage": {
                "depends_on": ["system"],
                "required_by": ["uploads"],
                "external_dependencies": []
            },
            "analytics": {
                "depends_on": ["api", "database"],
                "required_by": [],
                "external_dependencies": ["pandas", "numpy"]
            }
        }
        
        logger.info(
            "Dépendances des modules récupérées",
            extra={
                "tenant_id": tenant_id,
                "modules_count": len(dependencies),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "dependencies": dependencies,
            "graph": {
                "nodes": list(dependencies.keys()),
                "edges": [
                    {"from": module, "to": dep}
                    for module, info in dependencies.items()
                    for dep in info["depends_on"]
                ]
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération des dépendances: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur dépendances: {str(e)}")