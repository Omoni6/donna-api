from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    PLANIFI = "planifi"
    PUBLIE = "publie"
    CREE = "cree"
    COMMERCIAL = "commercial"

class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentExecutionRequest(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    instruction: str = Field(..., description="Instruction pour l'agent")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte additionnel")
    agent_type: Optional[AgentType] = Field(None, description="Type d'agent spécifique")
    priority: int = Field(default=1, ge=1, le=5, description="Priorité (1-5)")

class AgentExecutionResponse(BaseModel):
    task_id: str = Field(..., description="ID de la tâche")
    status: AgentStatus = Field(..., description="Statut de l'exécution")
    message: str = Field(..., description="Message de status")
    result: Optional[Dict[str, Any]] = Field(None, description="Résultat de l'exécution")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)

class AgentTaskStatus(BaseModel):
    task_id: str = Field(..., description="ID de la tâche")
    status: AgentStatus = Field(..., description="Statut actuel")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Progression (0-1)")
    message: Optional[str] = Field(None, description="Message de status")
    result: Optional[Dict[str, Any]] = Field(None, description="Résultat")
    error: Optional[str] = Field(None, description="Erreur si échec")
    started_at: Optional[datetime] = Field(None)
    completed_at: Optional[datetime] = Field(None)
    duration: Optional[float] = Field(None, description="Durée en secondes")

class AgentTaskList(BaseModel):
    tasks: List[AgentTaskStatus] = Field(default_factory=list)
    total: int = Field(..., description="Nombre total de tâches")
    page: int = Field(default=1, description="Page actuelle")
    page_size: int = Field(default=10, description="Taille de page")

class AgentConfig(BaseModel):
    agent_type: AgentType = Field(..., description="Type d'agent")
    name: str = Field(..., description="Nom de l'agent")
    description: Optional[str] = Field(None, description="Description")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration")
    is_active: bool = Field(default=True, description="Agent actif")
    max_concurrent_tasks: int = Field(default=1, ge=1, description="Tâches simultanées max")
    timeout_seconds: int = Field(default=300, ge=30, description="Timeout en secondes")