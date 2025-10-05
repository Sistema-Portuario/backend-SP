from sqlalchemy.orm import Session
from src.models.usuario import Usuario
import uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Configurações de segurança 
SECRET_KEY = "sua_chave_supersecreta"  # coloque no .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utilidades de senha
def gerar_hash(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha, hash_senha)

# Utilidades de token
def criar_token(usuario_id: str):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": usuario_id, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# CREATE
def criar_usuario(db: Session, nome: str, senha: str, cargo_id: uuid.UUID):
    hash_senha = gerar_hash(senha)
    novo_usuario = Usuario(nome=nome, senha=hash_senha, cargo_id=cargo_id)
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
        usuario.senha = gerar_hash(senha)
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

# LOGIN
def autenticar_usuario(db: Session, nome: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None
    return usuario
