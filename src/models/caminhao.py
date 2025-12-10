# models/caminhao.py
import uuid
import enum
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base_model import Base 

class StatusCaminhao(enum.Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    MANUTENCAO = "manutencao"

class Caminhao(Base):
    __tablename__ = 'caminhoes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    placa = Column(String, unique=True, nullable=False)
    motorista = Column(String)
    modelo = Column(String) # Opcional: Volvo, Scania, etc.
    status = Column(Enum(StatusCaminhao), default=StatusCaminhao.ATIVO)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())