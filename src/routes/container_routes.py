from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.containeres import criar_container, listar_containeres, buscar_container_por_id, atualizar_container, deletar_container
from src.schemas.container_schema import ContainerCreate, ContainerUpdate
from src.database.connection import get_db
import uuid

router = APIRouter(prefix="/containeres", tags=["Containeres"])

# CREATE
@router.post("/")
def criar(container: ContainerCreate, db: Session = Depends(get_db)):
    return criar_container(db, container)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_containeres(db)

@router.get("/{container_id}")
def buscar(container_id: uuid.UUID, db: Session = Depends(get_db)):
    container = buscar_container_por_id(db, container_id)
    if not container:
        raise HTTPException(status_code=404, detail="Container não encontrado")
    return container

# UPDATE - Esta é a rota que você usará para atualizar o status
@router.put("/{container_id}")
def atualizar(container_id: uuid.UUID, container_update: ContainerUpdate, db: Session = Depends(get_db)):
    container = atualizar_container(db, container_id, container_update)
    if not container:
        raise HTTPException(status_code=404, detail="Container não encontrado")
    return container

# DELETE
@router.delete("/{container_id}")
def deletar(container_id: uuid.UUID, db: Session = Depends(get_db)):
    container = deletar_container(db, container_id)
    if not container:
        raise HTTPException(status_code=404, detail="Container não encontrado")
    return {"detail": "Container deletado com sucesso"}