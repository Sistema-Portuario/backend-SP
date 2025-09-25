from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.navios import criar_navio, listar_navios, buscar_navio_por_id, atualizar_navio, deletar_navio
from src.database.connection import get_db
from src.schemas.manifesto_schema import ChegadaNavio
from src.schemas.navio_schema import NavioCompleto
from src.controllers.manifestos import registrar_chegada_navio
import uuid
from typing import Optional

router = APIRouter(prefix="/navios", tags=["Navios"])

# CREATE
@router.post("/")
def criar(nome: str, pais: str, capacidade: int, tipo: Optional[str] = None, db: Session = Depends(get_db)):
    return criar_navio(db, nome=nome, pais=pais, capacidade=capacidade, tipo=tipo)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_navios(db)

@router.get("/{navio_id}", response_model=NavioCompleto)
def buscar(navio_id: uuid.UUID, db: Session = Depends(get_db)):
    navio = buscar_navio_por_id(db, navio_id)
    if not navio:
        raise HTTPException(status_code=404, detail="Navio não encontrado")
    return navio

# UPDATE
@router.put("/{navio_id}")
def atualizar(navio_id: uuid.UUID, nome: Optional[str] = None, pais: Optional[str] = None, capacidade: Optional[int] = None, tipo: Optional[str] = None, db: Session = Depends(get_db)):
    navio = atualizar_navio(db, navio_id, nome, pais, capacidade, tipo)
    if not navio:
        raise HTTPException(status_code=404, detail="Navio não encontrado")
    return navio

# DELETE
@router.delete("/{navio_id}")
def deletar(navio_id: uuid.UUID, db: Session = Depends(get_db)):
    navio = deletar_navio(db, navio_id)
    if not navio:
        raise HTTPException(status_code=404, detail="Navio não encontrado")
    return {"detail": "Navio deletado com sucesso"}

# ROTA PARA REGISTRAR CHEGADA DE UM NAVIO
@router.post("/{navio_id}/chegada", summary="Registra a chegada de um navio com seus contêineres")
def registrar_chegada(navio_id: uuid.UUID, chegada: ChegadaNavio, db: Session = Depends(get_db)):
    manifesto, msg = registrar_chegada_navio(db, navio_id, chegada)
    if not manifesto:
        raise HTTPException(status_code=404, detail=msg)
    return {"detail": msg, "manifesto": manifesto}