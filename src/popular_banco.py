import sys
import os
import random
import unicodedata
from datetime import timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- CONFIGURAÇÃO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.models.base_model import Base 
from src.models.cargo import Cargo
from src.models.container import Container, StatusContainer
from src.models.localidade import Localidade
from src.models.manifesto import ManifestoCarga
from src.models.navio import Navio
from src.models.setor import Setor
from src.models.usuario import Usuario
from src.models.caminhao import Caminhao, StatusCaminhao
from src.models.credencial import Credencial

DB_URL = "postgresql://postgres:1234@localhost:5432/sistema_portuario"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker('pt_BR')

def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def resetar_banco():
    print("Resetando banco...", end=" ", flush=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("OK.")

def popular_banco():
    print("Populando dados...", end=" ", flush=True)
    
    # 1. CARGOS
    cargos_nomes = ['Gerente', 'Operador', 'Fiscal', 'TI', 'Estivador']
    cargos_db = []
    for nome in cargos_nomes:
        c = Cargo(nome=nome, descricao=fake.job())
        session.add(c)
        cargos_db.append(c)
    session.commit()
    if not cargos_db: cargos_db = session.query(Cargo).all()

    # 2. USUARIOS
    usuarios_novos = [] 
    for _ in range(10):
        if cargos_db: 
            u = Usuario(
                nome=fake.name(),
                senha=fake.password(),
                cargo_id=random.choice(cargos_db).id
            )
            session.add(u)
            usuarios_novos.append(u)
    session.commit()

    # 3. CREDENCIAIS
    for usuario in usuarios_novos:
        partes = remover_acentos(usuario.nome.lower()).split()
        base = f"{partes[0]}.{partes[-1]}" if len(partes) > 1 else partes[0]
        user = f"{base}{random.randint(10, 99)}"
        
        cred = Credencial(
            usuario_id=usuario.id,
            email_corporativo=f"{user}@portosystem.com.br",
            username_acesso=user
        )
        session.add(cred)
    session.commit()

    # 4. CAMINHÕES
    modelos = ['Volvo FH 540', 'Scania R450', 'Mercedes-Benz Actros', 'DAF XF', 'Iveco S-Way']
    status_opts = [StatusCaminhao.ATIVO, StatusCaminhao.INATIVO, StatusCaminhao.MANUTENCAO]
    
    for _ in range(15):
        c = Caminhao(
            placa=fake.license_plate(),
            motorista=fake.name(),
            modelo=random.choice(modelos),
            status=random.choice(status_opts)
        )
        session.add(c)
    session.commit()

    # 5. LOCALIDADES
    localidades_db = []
    for _ in range(5):
        l = Localidade(nome=f"Porto de {fake.city()}", cidade=fake.city(), pais=fake.country())
        session.add(l)
        localidades_db.append(l)
    session.commit()

    # 6. NAVIOS
    navios_db = []
    tipos = ['Cargueiro', 'Tanque', 'Porta-Contentores']
    for _ in range(5):
        n = Navio(
            nome=f"{fake.first_name()} {fake.color_name().capitalize()}",
            pais=fake.country(),
            capacidade=random.randint(100, 2000),
            tipo=random.choice(tipos)
        )
        session.add(n)
        navios_db.append(n)
    session.commit()

    # 7. MANIFESTOS 
    manifestos_db = []
    for i in range(30):
        if localidades_db and navios_db:
            origem = random.choice(localidades_db)
            destino = random.choice(localidades_db)
            while destino.id == origem.id and len(localidades_db) > 1:
                destino = random.choice(localidades_db)

            dt_chegada = fake.date_time_between(start_date='-10d', end_date='now')
            dt_saida = dt_chegada + timedelta(days=random.randint(1, 4))

            m = ManifestoCarga(
                navio_id=random.choice(navios_db).id,
                origem_id=origem.id,
                destino_id=destino.id,
                data_chegada=dt_chegada,
                data_saida=dt_saida
            )
            session.add(m)
            manifestos_db.append(m)
    session.commit()

    # 8. CONTAINERS
    ids_containers = []
    status_cont = [StatusContainer.CHEIO, StatusContainer.VAZIO, StatusContainer.AGUARDANDO]
    
    for _ in range(60):
        if manifestos_db:
            manif = random.choice(manifestos_db)
            c = Container(
                manifesto_id=manif.id,
                modelo='20 Pes',
                carga=fake.word(),
                tipo='Seco',
                status=random.choice(status_cont),
                peso=random.uniform(1000.0, 30000.0),
                created_at=manif.data_chegada
            )
            session.add(c)
            session.flush()
            ids_containers.append(c.id)
    
    # 9. SETORES
    for i in range(5):
        if localidades_db:
            qtd = random.randint(1, 3)
            amostra = random.sample(ids_containers, qtd) if len(ids_containers) >= qtd else []
            s = Setor(
                localidade_id=random.choice(localidades_db).id,
                capacidade=random.uniform(500.0, 2000.0),
                containeres=amostra
            )
            session.add(s)
    session.commit()

    print("OK.")

if __name__ == "__main__":
    try:
        resetar_banco()
        popular_banco()
    except Exception as e:
        print(f"\nErro: {e}")
        session.rollback()
    finally:
        session.close()