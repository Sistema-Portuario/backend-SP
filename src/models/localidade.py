import uuid
from sqlalchemy import Column, String, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.models.base_model import Base

class Localidade(Base):
    __tablename__ = 'localidades'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())