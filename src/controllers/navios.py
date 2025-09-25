from sqlalchemy.orm import Session, joinedload
from src.models import Navio, ManifestoCarga
import uuid
from typing import Optional

# CREATE
def criar_navio(db: Session, nome: str, pais: str, capacidade: int, tipo: Optional[str] = None):
    novo_navio = Navio(nome=nome, pais=pais, capacidade=capacidade, tipo=tipo)
    db.add(novo_navio)
    db.commit()
    db.refresh(novo_navio)
    return novo_navio

# READ (listar todos)
def listar_navios(db: Session):
    return db.query(Navio).all()

# READ (por ID)
def buscar_navio_por_id(db: Session, navio_id: uuid.UUID):
    return db.query(Navio).options(
        joinedload(Navio.manifestos).joinedload(ManifestoCarga.containeres)
    ).filter(Navio.id == navio_id).first()

# UPDATE
def atualizar_navio(db: Session, navio_id: uuid.UUID, nome: Optional[str] = None, pais: Optional[str] = None, capacidade: Optional[int] = None, tipo: Optional[str] = None):
    navio = db.query(Navio).filter(Navio.id == navio_id).first()
    if not navio:\
        return None
    if nome is not None:
        navio.nome = nome
    if pais is not None:
        navio.pais = pais
    if capacidade is not None:
        navio.capacidade = capacidade
    if tipo is not None:
        navio.tipo = tipo
    db.commit()
    db.refresh(navio)
    return navio

# DELETE
def deletar_navio(db: Session, navio_id: uuid.UUID):
    navio = db.query(Navio).filter(Navio.id == navio_id).first()
    if not navio:
        return None
    db.delete(navio)
    db.commit()
    return navio