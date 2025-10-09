from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid

from src.controllers.usuarios import (
    criar_usuario, listar_usuarios, buscar_usuario_por_id, 
    atualizar_usuario, deletar_usuario,
    autenticar_usuario, criar_token, validar_token
)
from src.database.connection import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

# CREATE 
@router.post("/")
def criar(nome: str, senha: str, cargo_id: uuid.UUID, db: Session = Depends(get_db)):
    return criar_usuario(db, nome, senha, cargo_id)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_usuarios(db)

# LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token(str(usuario.id))
    return {"access_token": token, "token_type": "bearer"}

# ROTA PROTEGIDA
@router.get("/me")
def perfil(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    usuario_id = validar_token(token)
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    usuario = buscar_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": usuario.id, "nome": usuario.nome}
    
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


