from pydantic import BaseModel
from src.models.container import StatusContainer
import uuid
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

# Schema para um contêiner que está chegando em um manifesto
class ContainerNaChegada(BaseModel):
    modelo: Optional[str] = None
    carga: Optional[str] = None
    tipo: Optional[str] = None
    status: StatusContainer = StatusContainer.EM_TRANSITO
    peso: Optional[Decimal] = None

# Schema principal para o payload da rota de chegada
class ChegadaNavio(BaseModel):
    origem_id: uuid.UUID
    destino_id: uuid.UUID
    data_chegada: datetime
    containeres: List[ContainerNaChegada] = []