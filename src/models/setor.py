import uuid
from sqlalchemy import Column, String, Float, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class Setor(Base):
    __tablename__ = 'setores'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    containeres = Column(ARRAY(UUID))
    capacidade = Column(Float)
    localidade_id = Column(UUID(as_uuid=True), ForeignKey('localidades.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    localidade = relationship("Localidade")