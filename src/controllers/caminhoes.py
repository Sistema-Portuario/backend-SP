from sqlalchemy.orm import Session
from src.models.caminhao import Caminhao
from src.schemas.caminhao_schema import CaminhaoCreate, CaminhaoUpdate
import uuid

def criar_caminhao(db: Session, caminhao: CaminhaoCreate):
    db_caminhao = Caminhao(**caminhao.dict())
    db.add(db_caminhao)
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

def listar_caminhoes(db: Session):
    return db.query(Caminhao).all()

def buscar_caminhao_por_id(db: Session, caminhao_id: uuid.UUID):
    return db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()

def atualizar_caminhao(db: Session, caminhao_id: uuid.UUID, caminhao_update: CaminhaoUpdate):
    db_caminhao = buscar_caminhao_por_id(db, caminhao_id)
    if not db_caminhao:
        return None
    
    # Atualiza apenas os campos que foram enviados (exclui os nulos)
    dados_atualizacao = caminhao_update.dict(exclude_unset=True)
    for key, value in dados_atualizacao.items():
        setattr(db_caminhao, key, value)
    
    db.commit()
    db.refresh(db_caminhao)
    return db_caminhao

def deletar_caminhao(db: Session, caminhao_id: uuid.UUID):
    db_caminhao = buscar_caminhao_por_id(db, caminhao_id)
    if not db_caminhao:
        return None
    
    db.delete(db_caminhao)
    db.commit()
    return db_caminhao