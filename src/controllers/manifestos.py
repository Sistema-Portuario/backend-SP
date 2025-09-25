from sqlalchemy.orm import Session
from src.models import Navio, ManifestoCarga, Container, Localidade
from src.schemas.manifesto_schema import ChegadaNavio, ContainerNaChegada
import uuid

def registrar_chegada_navio(db: Session, navio_id: uuid.UUID, chegada: ChegadaNavio):
    # 1. Valida se as entidades principais existem
    db_navio = db.query(Navio).filter(Navio.id == navio_id).first()
    if not db_navio:
        return None, "Navio não encontrado"

    db_origem = db.query(Localidade).filter(Localidade.id == chegada.origem_id).first()
    if not db_origem:
        return None, "Localidade de origem não encontrada"

    db_destino = db.query(Localidade).filter(Localidade.id == chegada.destino_id).first()
    if not db_destino:
        return None, "Localidade de destino não encontrada"

    # 2. Cria o manifesto de carga
    novo_manifesto = ManifestoCarga(
        navio_id=navio_id,
        origem_id=chegada.origem_id,
        destino_id=chegada.destino_id,
        data_chegada=chegada.data_chegada
    )
    db.add(novo_manifesto)
    db.flush() # Usa flush para obter o ID do manifesto antes do commit

    # 3. Cria os contêineres associados ao manifesto
    for container_data in chegada.containeres:
        novo_container = Container(
            **container_data.model_dump(),
            manifesto_id=novo_manifesto.id
        )
        db.add(novo_container)

    # 4. Salva tudo no banco de forma atômica
    db.commit()
    db.refresh(novo_manifesto)
    return novo_manifesto, "Chegada registrada com sucesso"