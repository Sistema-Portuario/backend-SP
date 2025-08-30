import uuid
from sqlalchemy import Column, String, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    cargo_id = Column(UUID(as_uuid=True), ForeignKey('cargos.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    cargo = relationship("Cargo")