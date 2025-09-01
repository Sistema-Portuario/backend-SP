from sqlalchemy.orm import Session
from src.models.usuario import Usuario
import uuid

# CREATE
def criar_usuario(db: Session, nome: str, senha: str, cargo_id: uuid.UUID):
    novo_usuario = Usuario(nome=nome, senha=senha, cargo_id=cargo_id)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# READ (listar todos)
def listar_usuarios(db: Session):
    return db.query(Usuario).all()

# READ (por ID)
def buscar_usuario_por_id(db: Session, usuario_id: uuid.UUID):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

# UPDATE
def atualizar_usuario(db: Session, usuario_id: uuid.UUID, nome: str = None, senha: str = None, cargo_id: uuid.UUID = None):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return None
    if nome:
        usuario.nome = nome
    if senha:
        usuario.senha = senha
    if cargo_id:
        usuario.cargo_id = cargo_id
    db.commit()
    db.refresh(usuario)
    return usuario

# DELETE
def deletar_usuario(db: Session, usuario_id: uuid.UUID):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return None
    db.delete(usuario)
    db.commit()
    return usuario
