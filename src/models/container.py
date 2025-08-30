import uuid
from sqlalchemy import Column, String, Enum, Numeric, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base_model import Base
import enum

class StatusContainer(enum.Enum):
    CHEIO = "cheio"
    VAZIO = "vazio"
    EM_TRANSITO = "em_transito"
    AGUARDANDO = "aguardando"

class Container(Base):
    __tablename__ = 'containeres'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manifesto_id = Column(UUID(as_uuid=True), ForeignKey('manifestos_carga.id'), nullable=False)
    modelo = Column(String)
    carga = Column(String) 
    tipo = Column(String)
    status = Column(Enum(StatusContainer), nullable=False, default=StatusContainer.AGUARDANDO)
    peso = Column(Numeric(10, 2)) # 10 dígitos no total, 2 casas decimais
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    manifesto = relationship("ManifestoCarga", back_populates="containeres")