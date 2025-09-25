from sqlalchemy.orm import Session
from src.models.setor import Setor
from src.schemas.setor_schema import SetorCreate, SetorUpdate
import uuid

# CREATE
def criar_setor(db: Session, setor: SetorCreate):
    novo_setor = Setor(**setor.model_dump())
    db.add(novo_setor)
    db.commit()
    db.refresh(novo_setor)
    return novo_setor

# READ (listar todos)
def listar_setores(db: Session):
    return db.query(Setor).all()

# READ (por ID)
def buscar_setor_por_id(db: Session, setor_id: uuid.UUID):
    return db.query(Setor).filter(Setor.id == setor_id).first()

# UPDATE
def atualizar_setor(db: Session, setor_id: uuid.UUID, setor_update: SetorUpdate):
    setor = db.query(Setor).filter(Setor.id == setor_id).first()
    if not setor:
        return None
    
    update_data = setor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(setor, key, value)
        
    db.commit()
    db.refresh(setor)
    return setor

# DELETE
def deletar_setor(db: Session, setor_id: uuid.UUID):
    setor = db.query(Setor).filter(Setor.id == setor_id).first()
    if not setor:
        return None
    db.delete(setor)
    db.commit()
    return setor