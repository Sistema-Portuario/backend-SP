import uuid
from sqlalchemy import Column, String, Integer, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.models.base_model import Base

class Navio(Base):
    __tablename__ = 'navios'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False, unique=True)
    pais = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False) # Capacidade em contêineres
    tipo = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())