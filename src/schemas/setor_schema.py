from pydantic import BaseModel
import uuid
from typing import Optional, List

# Molde para CRIAR um setor.
class SetorCreate(BaseModel):
    capacidade: float
    localidade_id: uuid.UUID
    # A lista de contêineres começa vazia por padrão
    containeres: List[uuid.UUID] = []

# Molde para ATUALIZAR um setor.
class SetorUpdate(BaseModel):
    capacidade: Optional[float] = None
    localidade_id: Optional[uuid.UUID] = None
    containeres: Optional[List[uuid.UUID]] = None