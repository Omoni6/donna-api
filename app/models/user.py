from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class User(BaseModel):
    id: str = Field(..., description="ID unique de l'utilisateur")
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    name: Optional[str] = Field(None, description="Nom complet")
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille")
    avatar: Optional[HttpUrl] = Field(None, description="URL de l'avatar")
    role: UserRole = Field(default=UserRole.USER, description="Rôle de l'utilisateur")
    status: UserStatus = Field(default=UserStatus.PENDING, description="Statut du compte")
    tenant_id: str = Field(..., description="ID du tenant")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)
    last_login: Optional[datetime] = Field(None, description="Dernière connexion")
    email_verified: bool = Field(default=False, description="Email vérifié")
    phone_verified: bool = Field(default=False, description="Téléphone vérifié")
    two_factor_enabled: bool = Field(default=False, description="2FA activé")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Préférences utilisateur")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Métadonnées")

class UserProfile(BaseModel):
    id: str = Field(..., description="ID de l'utilisateur")
    email: EmailStr = Field(..., description="Email")
    name: Optional[str] = Field(None, description="Nom complet")
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille")
    avatar: Optional[HttpUrl] = Field(None, description="Avatar")
    role: UserRole = Field(..., description="Rôle")
    status: UserStatus = Field(..., description="Statut")
    created_at: datetime = Field(..., description="Date de création")
    last_login: Optional[datetime] = Field(None, description="Dernière connexion")
    email_verified: bool = Field(..., description="Email vérifié")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Préférences")

class UserCreateRequest(BaseModel):
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    name: Optional[str] = Field(None, description="Nom complet")
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille")
    password: Optional[str] = Field(None, description="Mot de passe")
    role: UserRole = Field(default=UserRole.USER, description="Rôle")
    tenant_id: str = Field(..., description="ID du tenant")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Préférences")

class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="Nom complet")
    first_name: Optional[str] = Field(None, description="Prénom")
    last_name: Optional[str] = Field(None, description="Nom de famille")
    avatar: Optional[HttpUrl] = Field(None, description="Avatar")
    role: Optional[UserRole] = Field(None, description="Rôle")
    status: Optional[UserStatus] = Field(None, description="Statut")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Préférences")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées")

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Mot de passe")
    remember_me: bool = Field(default=False, description="Se souvenir de moi")

class UserLoginResponse(BaseModel):
    access_token: str = Field(..., description="Token d'accès")
    token_type: str = Field(default="bearer", description="Type de token")
    expires_in: int = Field(..., description="Expiration en secondes")
    user: UserProfile = Field(..., description="Profil utilisateur")

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="Email pour la réinitialisation")

class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="Token de réinitialisation")
    new_password: str = Field(..., min_length=8, description="Nouveau mot de passe")

class BusinessInfo(BaseModel):
    business_name: str = Field(..., description="Nom de l'entreprise")
    business_type: str = Field(..., description="Type d'entreprise")
    website: Optional[HttpUrl] = Field(None, description="Site web")
    phone: Optional[str] = Field(None, description="Téléphone")
    address: Optional[Dict[str, Any]] = Field(None, description="Adresse")
    industry: Optional[str] = Field(None, description="Industrie")
    size: Optional[str] = Field(None, description="Taille de l'entreprise")
    description: Optional[str] = Field(None, description="Description")

class UserOnboardingData(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    business_info: BusinessInfo = Field(..., description="Informations d'entreprise")
    goals: List[str] = Field(..., description="Objectifs")
    tools: List[str] = Field(..., description="Outils utilisés")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Préférences")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Métadonnées")