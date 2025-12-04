import uuid
from sqlalchemy import Column, String, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class Credencial(Base):
    __tablename__ = 'credenciais'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chave estrangeira ligando ao Usuario. 
    # unique=True garante que cada usuário só tenha 1 credencial (relação 1 para 1)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False, unique=True)
    
    email_corporativo = Column(String, nullable=False, unique=True)
    username_acesso = Column(String, nullable=False, unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relacionamento
    usuario = relationship("Usuario", back_populates="credencial")