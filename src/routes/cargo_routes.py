# src/routes/cargo_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.cargos import criar_cargo, listar_cargos, buscar_cargo_por_id, atualizar_cargo, deletar_cargo
from src.database.connection import get_db
import uuid

router = APIRouter(prefix="/cargos", tags=["Cargos"])

# CREATE
@router.post("/")
def criar(nome: str, descricao: str = None, db: Session = Depends(get_db)):
    return criar_cargo(db, nome, descricao)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_cargos(db)

@router.get("/{cargo_id}")
def buscar(cargo_id: uuid.UUID, db: Session = Depends(get_db)):
    cargo = buscar_cargo_por_id(db, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return cargo

# UPDATE
@router.put("/{cargo_id}")
def atualizar(cargo_id: uuid.UUID, nome: str = None, descricao: str = None, db: Session = Depends(get_db)):
    cargo = atualizar_cargo(db, cargo_id, nome, descricao)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return cargo

# DELETE
@router.delete("/{cargo_id}")
def deletar(cargo_id: uuid.UUID, db: Session = Depends(get_db)):
    cargo = deletar_cargo(db, cargo_id)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return {"detail": "Cargo deletado"}
