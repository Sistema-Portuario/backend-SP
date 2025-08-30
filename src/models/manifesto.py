import uuid
from sqlalchemy import Column, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class ManifestoCarga(Base):
    __tablename__ = 'manifestos_carga'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    navio_id = Column(UUID(as_uuid=True), ForeignKey('navios.id'), nullable=False)
    origem_id = Column(UUID(as_uuid=True), ForeignKey('localidades.id'), nullable=False)
    destino_id = Column(UUID(as_uuid=True), ForeignKey('localidades.id'), nullable=False)
    data_chegada = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    navio = relationship("Navio")
    origem = relationship("Localidade", foreign_keys=[origem_id])
    destino = relationship("Localidade", foreign_keys=[destino_id])
    containeres = relationship("Container", back_populates="manifesto")