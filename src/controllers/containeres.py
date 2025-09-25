from sqlalchemy.orm import Session
from src.models.container import Container
from src.schemas.container_schema import ContainerCreate, ContainerUpdate
import uuid

# CREATE: Usa o schema para criar um novo contêiner
def criar_container(db: Session, container: ContainerCreate):
    # O container.model_dump() desempacota o schema nos campos do modelo
    novo_container = Container(**container.model_dump())
    db.add(novo_container)
    db.commit()
    db.refresh(novo_container)
    return novo_container

# READ (listar todos)
def listar_containeres(db: Session):
    return db.query(Container).all()

# READ (por ID)
def buscar_container_por_id(db: Session, container_id: uuid.UUID):
    return db.query(Container).filter(Container.id == container_id).first()

# UPDATE: Usa o schema de update para atualizar os campos
def atualizar_container(db: Session, container_id: uuid.UUID, container_update: ContainerUpdate):
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None
    
    # Pega apenas os dados que foram enviados na requisição
    update_data = container_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(container, key, value) # Atualiza cada campo no objeto do banco
        
    db.commit()
    db.refresh(container)
    return container

# DELETE
def deletar_container(db: Session, container_id: uuid.UUID):
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None
    db.delete(container)
    db.commit()
    return container