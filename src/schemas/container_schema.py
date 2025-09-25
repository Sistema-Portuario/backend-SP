from pydantic import BaseModel
from src.models.container import StatusContainer
import uuid
from typing import Optional
from decimal import Decimal

# Molde para CRIAR um contêiner.
# manifesto_id é obrigatório para associar ao navio.
class ContainerCreate(BaseModel):
    manifesto_id: uuid.UUID
    modelo: Optional[str] = None
    carga: Optional[str] = None
    tipo: Optional[str] = None
    status: StatusContainer = StatusContainer.AGUARDANDO
    peso: Optional[Decimal] = None

# Molde para ATUALIZAR um contêiner.
# Todos os campos são opcionais, assim você pode atualizar só o status, por exemplo.
class ContainerUpdate(BaseModel):
    manifesto_id: Optional[uuid.UUID] = None
    modelo: Optional[str] = None
    carga: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[StatusContainer] = None
    peso: Optional[Decimal] = None