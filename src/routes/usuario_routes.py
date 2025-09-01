from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.usuarios import criar_usuario, listar_usuarios, buscar_usuario_por_id, atualizar_usuario, deletar_usuario
from src.database.connection import get_db
import uuid

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# CREATE
@router.post("/")
def criar(nome: str, senha: str, cargo_id: uuid.UUID, db: Session = Depends(get_db)):
    return criar_usuario(db, nome, senha, cargo_id)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_usuarios(db)

@router.get("/{usuario_id}")
def buscar(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# UPDATE
@router.put("/{usuario_id}")
def atualizar(usuario_id: uuid.UUID, nome: str = None, senha: str = None, cargo_id: uuid.UUID = None, db: Session = Depends(get_db)):
    usuario = atualizar_usuario(db, usuario_id, nome, senha, cargo_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# DELETE
@router.delete("/{usuario_id}")
def deletar(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = deletar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"detail": "Usuário deletado"}
