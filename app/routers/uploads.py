from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from typing import Optional, Dict, Any, List
import os
import uuid
import logging
from datetime import datetime
from ..core.security import get_tenant_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/uploads", tags=["uploads"])

# Configuration des uploads
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md'],
    'data': ['.json', '.csv', '.xlsx', '.xml'],
    'audio': ['.mp3', '.wav', '.m4a'],
    'video': ['.mp4', '.avi', '.mov']
}

def get_file_extension(filename: str) -> str:
    """Obtenir l'extension du fichier"""
    return os.path.splitext(filename)[1].lower()

def validate_file_type(filename: str, content_type: str) -> str:
    """Valider le type de fichier"""
    ext = get_file_extension(filename)
    
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    
    # Vérifier aussi le content-type
    if content_type.startswith('image/'):
        return 'image'
    elif content_type.startswith('application/pdf'):
        return 'document'
    elif content_type.startswith('text/'):
        return 'document'
    elif content_type.startswith('audio/'):
        return 'audio'
    elif content_type.startswith('video/'):
        return 'video'
    
    return 'unknown'

@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    tenant_id: Optional[str] = Depends(get_tenant_id),
    description: Optional[str] = Form(None)
):
    """Uploader un fichier unique"""
    try:
        # Valider la taille du fichier
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Valider le type de fichier
        file_type = validate_file_type(file.filename, file.content_type)
        if file_type == 'unknown':
            raise HTTPException(
                status_code=400,
                detail="Type de fichier non supporté"
            )
        
        # Générer un nom de fichier unique
        file_id = str(uuid.uuid4())
        file_extension = get_file_extension(file.filename)
        unique_filename = f"{file_id}{file_extension}"
        
        # Créer le répertoire d'upload si nécessaire
        upload_path = os.path.join(UPLOAD_DIR, tenant_id or "default", file_type)
        os.makedirs(upload_path, exist_ok=True)
        
        # Sauvegarder le fichier
        file_path = os.path.join(upload_path, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Créer les métadonnées
        file_info = {
            "id": file_id,
            "original_name": file.filename,
            "unique_name": unique_filename,
            "file_type": file_type,
            "content_type": file.content_type,
            "size": len(contents),
            "path": file_path,
            "description": description,
            "tenant_id": tenant_id,
            "uploaded_at": datetime.utcnow().isoformat() + "Z"
        }
        
        logger.info(
            "Fichier uploadé avec succès",
            extra={
                "file_id": file_id,
                "filename": file.filename,
                "file_type": file_type,
                "size": len(contents),
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "message": "Fichier uploadé avec succès",
            "file": file_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de l'upload du fichier: {str(e)}",
            extra={
                "filename": file.filename if hasattr(file, 'filename') else "unknown",
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur upload: {str(e)}")

@router.post("/files")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    tenant_id: Optional[str] = Depends(get_tenant_id),
    description: Optional[str] = Form(None)
):
    """Uploader plusieurs fichiers"""
    try:
        uploaded_files = []
        
        for file in files:
            try:
                # Valider la taille
                contents = await file.read()
                if len(contents) > MAX_FILE_SIZE:
                    logger.warning(
                        f"Fichier trop volumineux ignoré: {file.filename}",
                        extra={
                            "filename": file.filename,
                            "size": len(contents),
                            "tenant_id": tenant_id
                        }
                    )
                    continue
                
                # Valider le type
                file_type = validate_file_type(file.filename, file.content_type)
                if file_type == 'unknown':
                    logger.warning(
                        f"Type de fichier non supporté ignoré: {file.filename}",
                        extra={
                            "filename": file.filename,
                            "content_type": file.content_type,
                            "tenant_id": tenant_id
                        }
                    )
                    continue
                
                # Générer nom unique et sauvegarder
                file_id = str(uuid.uuid4())
                file_extension = get_file_extension(file.filename)
                unique_filename = f"{file_id}{file_extension}"
                
                upload_path = os.path.join(UPLOAD_DIR, tenant_id or "default", file_type)
                os.makedirs(upload_path, exist_ok=True)
                
                file_path = os.path.join(upload_path, unique_filename)
                with open(file_path, 'wb') as f:
                    f.write(contents)
                
                file_info = {
                    "id": file_id,
                    "original_name": file.filename,
                    "unique_name": unique_filename,
                    "file_type": file_type,
                    "content_type": file.content_type,
                    "size": len(contents),
                    "path": file_path,
                    "description": description,
                    "tenant_id": tenant_id,
                    "uploaded_at": datetime.utcnow().isoformat() + "Z"
                }
                
                uploaded_files.append(file_info)
                
            except Exception as e:
                logger.error(
                    f"Erreur lors de l'upload du fichier {file.filename}: {str(e)}",
                    extra={
                        "filename": file.filename,
                        "tenant_id": tenant_id,
                        "error": str(e)
                    }
                )
                continue
        
        logger.info(
            "Upload multiple fichiers terminé",
            extra={
                "files_count": len(uploaded_files),
                "total_files": len(files),
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "message": f"{len(uploaded_files)} fichiers uploadés avec succès",
            "files": uploaded_files,
            "total_processed": len(files),
            "successful": len(uploaded_files)
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de l'upload multiple: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur upload multiple: {str(e)}")

@router.get("/files")
async def list_uploaded_files(
    tenant_id: Optional[str] = Depends(get_tenant_id),
    file_type: Optional[str] = None,
    limit: int = 50
):
    """Lister les fichiers uploadés"""
    try:
        files = []
        base_path = os.path.join(UPLOAD_DIR, tenant_id or "default")
        
        if not os.path.exists(base_path):
            return {
                "status": "success",
                "files": [],
                "total": 0,
                "message": "Aucun fichier trouvé"
            }
        
        # Parcourir les répertoires par type
        search_types = [file_type] if file_type else ALLOWED_EXTENSIONS.keys()
        
        for file_type_dir in search_types:
            type_path = os.path.join(base_path, file_type_dir)
            if os.path.exists(type_path):
                for filename in os.listdir(type_path):
                    file_path = os.path.join(type_path, filename)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        files.append({
                            "filename": filename,
                            "file_type": file_type_dir,
                            "size": stat.st_size,
                            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat() + "Z",
                            "path": file_path
                        })
        
        # Trier par date de création (décroissant) et limiter
        files.sort(key=lambda x: x["created_at"], reverse=True)
        files = files[:limit]
        
        logger.info(
            "Liste des fichiers récupérée",
            extra={
                "files_count": len(files),
                "tenant_id": tenant_id,
                "file_type": file_type,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "status": "success",
            "files": files,
            "total": len(files),
            "tenant_id": tenant_id
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération de la liste des fichiers: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur liste fichiers: {str(e)}")

@router.delete("/files/{filename}")
async def delete_file(
    filename: str,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """Supprimer un fichier uploadé"""
    try:
        # Trouver le fichier dans les répertoires
        base_path = os.path.join(UPLOAD_DIR, tenant_id or "default")
        file_deleted = False
        
        for file_type_dir in ALLOWED_EXTENSIONS.keys():
            type_path = os.path.join(base_path, file_type_dir)
            file_path = os.path.join(type_path, filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                file_deleted = True
                
                logger.info(
                    "Fichier supprimé avec succès",
                    extra={
                        "filename": filename,
                        "file_path": file_path,
                        "tenant_id": tenant_id,
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                )
                break
        
        if not file_deleted:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        return {
            "status": "success",
            "message": f"Fichier {filename} supprimé avec succès",
            "filename": filename,
            "tenant_id": tenant_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la suppression du fichier: {str(e)}",
            extra={
                "filename": filename,
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")

@router.get("/config")
async def get_upload_config():
    """Obtenir la configuration des uploads"""
    return {
        "max_file_size": MAX_FILE_SIZE,
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
        "allowed_extensions": ALLOWED_EXTENSIONS,
        "supported_types": list(ALLOWED_EXTENSIONS.keys())
    }