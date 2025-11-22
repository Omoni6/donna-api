from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
import logging
import uuid
from datetime import datetime

from app.models.agent import (
    AgentExecutionRequest, 
    AgentExecutionResponse, 
    AgentTaskStatus,
    AgentType
)
from app.services.agent_zero import agent_zero_service
from app.core.security import verify_api_key, get_current_user, get_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("/execute", response_model=AgentExecutionResponse)
async def execute_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Exécute un agent via Donna Worker
    
    Args:
        request: Requête d'exécution d'agent
        background_tasks: Tâches d'arrière-plan
        api_key: Clé API pour l'authentification
        tenant_id: ID du tenant
    
    Returns:
        Réponse de l'exécution de l'agent
    """
    try:
        logger.info(f"🚀 Exécution de l'agent pour l'utilisateur {request.user_id} - Tenant: {tenant_id}")
        
        # Ajouter le tenant_id au contexte
        request.context["tenant_id"] = tenant_id
        
        # Exécuter l'agent en arrière-plan pour une réponse rapide
        background_tasks.add_task(
            agent_zero_service.execute_agent_task,
            request
        )
        
        # Retourner une réponse immédiate avec l'ID de tâche
        return AgentExecutionResponse(
            task_id="task_" + str(uuid.uuid4()),
            status="pending",
            message="Tâche d'agent en cours d'exécution",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de l'agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")

@router.get("/status/{task_id}", response_model=AgentTaskStatus)
async def get_agent_status(
    task_id: str,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Récupère le statut d'une tâche d'agent
    
    Args:
        task_id: ID de la tâche
        api_key: Clé API pour l'authentification
        tenant_id: ID du tenant
    
    Returns:
        Statut de la tâche
    """
    try:
        logger.info(f"📊 Récupération du statut de la tâche: {task_id} - Tenant: {tenant_id}")
        
        status = await agent_zero_service.get_task_status(task_id)
        return status
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération du statut: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du statut: {str(e)}")

@router.post("/planifi", response_model=AgentExecutionResponse)
async def execute_planifi_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """Exécute l'agent Planifi"""
    try:
        logger.info(f"📅 Exécution de l'agent Planifi pour l'utilisateur {request.user_id}")
        
        request.agent_type = AgentType.PLANIFI
        request.context["tenant_id"] = tenant_id
        
        background_tasks.add_task(
            agent_zero_service.planifi_agent,
            request.user_id,
            request.instruction,
            request.context
        )
        
        return AgentExecutionResponse(
            task_id="task_" + str(uuid.uuid4()),
            status="pending",
            message="Agent Planifi en cours d'exécution",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de l'agent Planifi: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")

@router.post("/publie", response_model=AgentExecutionResponse)
async def execute_publie_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """Exécute l'agent Publie"""
    try:
        logger.info(f"📢 Exécution de l'agent Publie pour l'utilisateur {request.user_id}")
        
        request.agent_type = AgentType.PUBLIE
        request.context["tenant_id"] = tenant_id
        
        background_tasks.add_task(
            agent_zero_service.publie_agent,
            request.user_id,
            request.instruction,
            request.context
        )
        
        return AgentExecutionResponse(
            task_id="task_" + str(uuid.uuid4()),
            status="pending",
            message="Agent Publie en cours d'exécution",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de l'agent Publie: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")

@router.post("/cree", response_model=AgentExecutionResponse)
async def execute_cree_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """Exécute l'agent Cree"""
    try:
        logger.info(f"🎨 Exécution de l'agent Cree pour l'utilisateur {request.user_id}")
        
        request.agent_type = AgentType.CREE
        request.context["tenant_id"] = tenant_id
        
        background_tasks.add_task(
            agent_zero_service.cree_agent,
            request.user_id,
            request.instruction,
            request.context
        )
        
        return AgentExecutionResponse(
            task_id="task_" + str(uuid.uuid4()),
            status="pending",
            message="Agent Cree en cours d'exécution",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de l'agent Cree: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")

@router.post("/commercial", response_model=AgentExecutionResponse)
async def execute_commercial_agent(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """Exécute l'agent Commercial"""
    try:
        logger.info(f"💼 Exécution de l'agent Commercial pour l'utilisateur {request.user_id}")
        
        request.agent_type = AgentType.COMMERCIAL
        request.context["tenant_id"] = tenant_id
        
        background_tasks.add_task(
            agent_zero_service.commercial_agent,
            request.user_id,
            request.instruction,
            request.context
        )
        
        return AgentExecutionResponse(
            task_id="task_" + str(uuid.uuid4()),
            status="pending",
            message="Agent Commercial en cours d'exécution",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de l'agent Commercial: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")

@router.get("/configs")
async def get_agent_configs(
    api_key: str = Depends(verify_api_key),
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Récupère la configuration des agents disponibles
    
    Args:
        api_key: Clé API pour l'authentification
        tenant_id: ID du tenant
    
    Returns:
        Configuration des agents
    """
    try:
        logger.info(f"⚙️ Récupération de la configuration des agents - Tenant: {tenant_id}")
        
        # Configuration des agents disponibles
        configs = {
            "agents": [
                {
                    "type": "planifi",
                    "name": "Agent Planifi",
                    "description": "Agent de planification et organisation",
                    "is_active": True,
                    "max_concurrent_tasks": 3,
                    "timeout_seconds": 300
                },
                {
                    "type": "publie", 
                    "name": "Agent Publie",
                    "description": "Agent de publication et diffusion",
                    "is_active": True,
                    "max_concurrent_tasks": 5,
                    "timeout_seconds": 600
                },
                {
                    "type": "cree",
                    "name": "Agent Cree", 
                    "description": "Agent de création de contenu",
                    "is_active": True,
                    "max_concurrent_tasks": 2,
                    "timeout_seconds": 900
                },
                {
                    "type": "commercial",
                    "name": "Agent Commercial",
                    "description": "Agent commercial et ventes",
                    "is_active": True,
                    "max_concurrent_tasks": 4,
                    "timeout_seconds": 180
                }
            ]
        }
        
        return configs
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des configurations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")