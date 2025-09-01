from sqlalchemy.orm import Session
from src.models.cargo import Cargo
import uuid

# CREATE
def criar_cargo(db: Session, nome: str, descricao: str = None):
    novo_cargo = Cargo(nome=nome, descricao=descricao)
    db.add(novo_cargo)
    db.commit()
    db.refresh(novo_cargo)
    return novo_cargo

# READ (listar todos)
def listar_cargos(db: Session):
    return db.query(Cargo).all()

# READ (por ID)
def buscar_cargo_por_id(db: Session, cargo_id: uuid.UUID):
    return db.query(Cargo).filter(Cargo.id == cargo_id).first()

# UPDATE
def atualizar_cargo(db: Session, cargo_id: uuid.UUID, nome: str = None, descricao: str = None):
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        return None
    if nome:
        cargo.nome = nome
    if descricao:
        cargo.descricao = descricao
    db.commit()
    db.refresh(cargo)
    return cargo

# DELETE
def deletar_cargo(db: Session, cargo_id: uuid.UUID):
    cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        return None
    db.delete(cargo)
    db.commit()
    return cargo
