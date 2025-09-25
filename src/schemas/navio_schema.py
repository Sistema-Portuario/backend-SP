from pydantic import BaseModel, ConfigDict
import uuid
from typing import List, Optional
from datetime import datetime

# Schema base para contêiner, para evitar referência circular
class ContainerSimples(BaseModel):
    id: uuid.UUID
    modelo: Optional[str]
    carga: Optional[str]

# Schema para Manifesto, incluindo seus contêineres
class ManifestoComContaineres(BaseModel):
    id: uuid.UUID
    origem_id: uuid.UUID
    destino_id: uuid.UUID
    data_chegada: datetime
    containeres: List[ContainerSimples] = []

# Schema final para Navio, incluindo seus manifestos
class NavioCompleto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    nome: str
    pais: str
    capacidade: int
    manifestos: List[ManifestoComContaineres] = []  