from pydantic import BaseModel
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

# Define os status permitidos (deve bater com o Model/Banco)
class StatusCaminhaoEnum(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    MANUTENCAO = "manutencao"

# Base: Campos comuns
class CaminhaoBase(BaseModel):
    placa: str
    motorista: str
    modelo: Optional[str] = None
    status: StatusCaminhaoEnum = StatusCaminhaoEnum.ATIVO

# Create: Usado no POST (criação)
class CaminhaoCreate(CaminhaoBase):
    pass

# Update: Usado no PUT (atualização)
# Todos os campos são opcionais para permitir atualização parcial
class CaminhaoUpdate(BaseModel):
    placa: Optional[str] = None
    motorista: Optional[str] = None
    modelo: Optional[str] = None
    status: Optional[StatusCaminhaoEnum] = None

# Response: Usado no retorno (GET/POST)
# Inclui ID e datas que o banco gera automaticamente
class CaminhaoResponse(CaminhaoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True