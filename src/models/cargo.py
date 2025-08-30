import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.models.base_model import Base

class Cargo(Base):
    __tablename__ = 'cargos'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String)