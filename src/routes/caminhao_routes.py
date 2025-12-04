from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import Optional

# Imports dos controllers e schemas
from src.database.connection import get_db
from src.controllers.caminhoes import criar_caminhao, listar_caminhoes, buscar_caminhao_por_id, atualizar_caminhao, deletar_caminhao
from src.schemas.caminhao_schema import CaminhaoResponse, CaminhaoCreate, CaminhaoUpdate

router = APIRouter(prefix="/caminhoes", tags=["Caminhões"])

# CREATE
@router.post("/")
def criar(
    placa: str, 
    motorista: str, 
    modelo: Optional[str] = None, 
    status: Optional[str] = "ativo", 
    db: Session = Depends(get_db)
):
    caminhao_in = CaminhaoCreate(
        placa=placa, 
        motorista=motorista, 
        modelo=modelo, 
        status=status
    )
    return criar_caminhao(db, caminhao_in)

# READ
@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_caminhoes(db)

@router.get("/{caminhao_id}", response_model=CaminhaoResponse)
def buscar(caminhao_id: uuid.UUID, db: Session = Depends(get_db)):
    caminhao = buscar_caminhao_por_id(db, caminhao_id)
    if not caminhao:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return caminhao

# UPDATE
# Padrão Navios: Recebe campos opcionais individuais
@router.put("/{caminhao_id}")
def atualizar(
    caminhao_id: uuid.UUID, 
    placa: Optional[str] = None, 
    motorista: Optional[str] = None, 
    modelo: Optional[str] = None, 
    status: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    caminhao_update = CaminhaoUpdate(
        placa=placa, 
        motorista=motorista, 
        modelo=modelo, 
        status=status
    )
    
    caminhao = atualizar_caminhao(db, caminhao_id, caminhao_update)
    if not caminhao:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return caminhao

# DELETE
@router.delete("/{caminhao_id}")
def deletar(caminhao_id: uuid.UUID, db: Session = Depends(get_db)):
    caminhao = deletar_caminhao(db, caminhao_id)
    if not caminhao:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return {"detail": "Caminhão deletado com sucesso"}