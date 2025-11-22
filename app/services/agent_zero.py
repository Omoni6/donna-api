import httpx
import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.agent import (
    AgentExecutionRequest, 
    AgentExecutionResponse, 
    AgentTaskStatus,
    AgentStatus,
    AgentType
)

logger = logging.getLogger(__name__)

class AgentZeroService:
    """Service pour communiquer avec Donna Worker (Agent Zero)"""
    
    def __init__(self):
        self.base_url = settings.DONNA_WORKER_URL
        self.timeout = 30.0
        self.logger = logging.getLogger(__name__)
    
    async def run_agent(self, instruction: str, context: Dict[str, Any], 
                       user_id: str, agent_type: Optional[AgentType] = None) -> AgentExecutionResponse:
        """
        Exécute un agent via Donna Worker
        
        Args:
            instruction: L'instruction à exécuter
            context: Le contexte de l'exécution
            user_id: ID de l'utilisateur
            agent_type: Type d'agent spécifique (optionnel)
        
        Returns:
            AgentExecutionResponse: Réponse de l'exécution
        """
        task_id = str(uuid.uuid4())
        
        try:
            payload = {
                "instruction": instruction,
                "context": context,
                "user_id": user_id,
                "agent_type": agent_type.value if agent_type else None,
                "task_id": task_id
            }
            
            self.logger.info(f"🚀 Envoi de la tâche à Donna Worker: {task_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": settings.API_KEY
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Tâche réussie: {task_id}")
                    
                    return AgentExecutionResponse(
                        task_id=task_id,
                        status=AgentStatus.COMPLETED,
                        message="Agent exécuté avec succès",
                        result=result,
                        created_at=datetime.utcnow()
                    )
                else:
                    error_msg = f"Erreur Donna Worker: {response.status_code} - {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    
                    return AgentExecutionResponse(
                        task_id=task_id,
                        status=AgentStatus.FAILED,
                        message=error_msg,
                        created_at=datetime.utcnow()
                    )
                    
        except httpx.TimeoutException:
            self.logger.error(f"⏰ Timeout lors de l'appel à Donna Worker: {task_id}")
            return AgentExecutionResponse(
                task_id=task_id,
                status=AgentStatus.FAILED,
                message="Timeout lors de l'exécution de l'agent",
                created_at=datetime.utcnow()
            )
        
        except Exception as e:
            self.logger.error(f"❌ Erreur inattendue: {str(e)}", exc_info=True)
            return AgentExecutionResponse(
                task_id=task_id,
                status=AgentStatus.FAILED,
                message=f"Erreur inattendue: {str(e)}",
                created_at=datetime.utcnow()
            )
    
    async def get_task_status(self, task_id: str) -> AgentTaskStatus:
        """
        Récupère le statut d'une tâche
        
        Args:
            task_id: ID de la tâche
        
        Returns:
            AgentTaskStatus: Statut de la tâche
        """
        # Pour l'instant, on retourne un statut simulé
        # Dans une vraie implémentation, on irait chercher dans Redis ou une base de données
        
        return AgentTaskStatus(
            task_id=task_id,
            status=AgentStatus.COMPLETED,
            progress=1.0,
            message="Tâche terminée",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            duration=5.0
        )
    
    async def execute_agent_task(self, request: AgentExecutionRequest) -> AgentExecutionResponse:
        """
        Exécute une tâche d'agent avec validation
        
        Args:
            request: Requête d'exécution d'agent
        
        Returns:
            AgentExecutionResponse: Réponse de l'exécution
        """
        self.logger.info(f"🔄 Exécution de l'agent {request.agent_type} pour l'utilisateur {request.user_id}")
        
        # Appeler Donna Worker
        response = await self.run_agent(
            instruction=request.instruction,
            context=request.context,
            user_id=request.user_id,
            agent_type=request.agent_type
        )
        
        # Log supplémentaire pour le suivi
        self.logger.info(
            f"📊 Agent exécuté - Task: {response.task_id}, "
            f"Status: {response.status}, Message: {response.message}"
        )
        
        return response
    
    async def planifi_agent(self, user_id: str, instruction: str, context: Dict[str, Any]) -> AgentExecutionResponse:
        """Exécute l'agent Planifi"""
        return await self.run_agent(
            instruction=instruction,
            context=context,
            user_id=user_id,
            agent_type=AgentType.PLANIFI
        )
    
    async def publie_agent(self, user_id: str, instruction: str, context: Dict[str, Any]) -> AgentExecutionResponse:
        """Exécute l'agent Publie"""
        return await self.run_agent(
            instruction=instruction,
            context=context,
            user_id=user_id,
            agent_type=AgentType.PUBLIE
        )
    
    async def cree_agent(self, user_id: str, instruction: str, context: Dict[str, Any]) -> AgentExecutionResponse:
        """Exécute l'agent Cree"""
        return await self.run_agent(
            instruction=instruction,
            context=context,
            user_id=user_id,
            agent_type=AgentType.CREE
        )
    
    async def commercial_agent(self, user_id: str, instruction: str, context: Dict[str, Any]) -> AgentExecutionResponse:
        """Exécute l'agent Commercial"""
        return await self.run_agent(
            instruction=instruction,
            context=context,
            user_id=user_id,
            agent_type=AgentType.COMMERCIAL
        )

# Singleton instance
agent_zero_service = AgentZeroService()