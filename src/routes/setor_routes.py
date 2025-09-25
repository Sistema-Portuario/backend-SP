from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.setores import (
    criar_setor, listar_setores, buscar_setor_por_id, 
    atualizar_setor, deletar_setor
)
from src.schemas.setor_schema import SetorCreate, SetorUpdate
from src.database.connection import get_db
import uuid

router = APIRouter(prefix="/setores", tags=["Setores"])

# CREATE
@router.post("/")
def criar(setor: SetorCreate, db: Session = Depends(get_db)):
    return criar_setor(db, setor)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_setores(db)

@router.get("/{setor_id}")
def buscar(setor_id: uuid.UUID, db: Session = Depends(get_db)):
    setor = buscar_setor_por_id(db, setor_id)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return setor

# UPDATE
@router.put("/{setor_id}")
def atualizar(setor_id: uuid.UUID, setor_update: SetorUpdate, db: Session = Depends(get_db)):
    setor = atualizar_setor(db, setor_id, setor_update)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return setor

# DELETE
@router.delete("/{setor_id}")
def deletar(setor_id: uuid.UUID, db: Session = Depends(get_db)):
    setor = deletar_setor(db, setor_id)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return {"detail": "Setor deletado com sucesso"}