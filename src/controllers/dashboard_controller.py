from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, Date
from datetime import datetime, timedelta

# Imports dos modelos e conexão
from src.database.connection import get_db
from src.models.manifesto import ManifestoCarga
from src.models.container import Container, StatusContainer
from src.models.caminhao import Caminhao, StatusCaminhao
from src.models.navio import Navio

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# ==============================================================================
# 1. ENDPOINT: RESUMO GERAL (KPIs)
# Rota: GET /dashboard/kpis
# ==============================================================================
@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Navios Chegados (Hoje)
    navios_chegados = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_chegada >= hoje
    ).scalar() or 0

    # Navios Saídos (Hoje) 
    navios_saidos = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_saida >= hoje
    ).scalar() or 0

    # Contêineres no Pátio (Estoque Atual - Diferente de EM_TRANSITO)
    containers_patio = db.query(func.count(Container.id)).filter(
        Container.status != StatusContainer.EM_TRANSITO
    ).scalar() or 0

    # Caminhões Ativos (Frota Total com status ATIVO)
    caminhoes_ativos = db.query(func.count(Caminhao.id)).filter(
        Caminhao.status == StatusCaminhao.ATIVO
    ).scalar() or 0

    return {
        "naviosChegados": navios_chegados,
        "naviosSaidos": navios_saidos, 
        "containersPatio": containers_patio,
        "caminhoesAtivos": caminhoes_ativos
    }

# ==============================================================================
# 2. ENDPOINT: COMPARAÇÃO SEMANAL
# Rota: GET /dashboard/comparacao
# ==============================================================================
@router.get("/comparacao")
def get_comparacao(db: Session = Depends(get_db)):
    agora = datetime.now()
    inicio_semana_atual = agora - timedelta(days=7)
    inicio_semana_anterior = agora - timedelta(days=14)

    def calcular_variacao(atual, anterior):
        if anterior == 0: return 100.0 if atual > 0 else 0.0
        return ((atual - anterior) / anterior) * 100.0

    # --- A. NAVIOS CHEGADOS ---
    navios_atual = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_chegada >= inicio_semana_atual
    ).scalar() or 0
    navios_anterior = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_chegada >= inicio_semana_anterior,
        ManifestoCarga.data_chegada < inicio_semana_atual
    ).scalar() or 0

    # --- B. NAVIOS SAÍDOS ---
    saidos_atual = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_saida >= inicio_semana_atual
    ).scalar() or 0
    saidos_anterior = db.query(func.count(ManifestoCarga.id)).filter(
        ManifestoCarga.data_saida >= inicio_semana_anterior,
        ManifestoCarga.data_saida < inicio_semana_atual
    ).scalar() or 0

    # --- C. CONTÊINERES (Entradas/Fluxo) ---
    containers_atual = db.query(func.count(Container.id)).filter(
        Container.created_at >= inicio_semana_atual
    ).scalar() or 0
    containers_anterior = db.query(func.count(Container.id)).filter(
        Container.created_at >= inicio_semana_anterior, 
        Container.created_at < inicio_semana_atual
    ).scalar() or 0

    # --- D. CAMINHÕES (Estabilidade) ---
    caminhoes_ativos = db.query(func.count(Caminhao.id)).filter(
        Caminhao.status == StatusCaminhao.ATIVO
    ).scalar() or 0

    return {
        "naviosChegados": {
            "atual": navios_atual, 
            "anterior": navios_anterior, 
            "variacao": calcular_variacao(navios_atual, navios_anterior)
        },
        "naviosSaidos": {
            "atual": saidos_atual, 
            "anterior": saidos_anterior, 
            "variacao": calcular_variacao(saidos_atual, saidos_anterior)
        },
        "containersPatio": {
            "atual": containers_atual, 
            "anterior": containers_anterior, 
            "variacao": calcular_variacao(containers_atual, containers_anterior)
        },
        "caminhoesAtivos": {
            "atual": caminhoes_ativos, 
            "anterior": caminhoes_ativos, 
            "variacao": 0.0
        }
    }

# ==============================================================================
# 3. ENDPOINT: GRÁFICOS (ÚLTIMOS 7 DIAS)
# Rota: GET /dashboard/graficos
# ==============================================================================
@router.get("/graficos")
def get_graficos(db: Session = Depends(get_db)):
    agora = datetime.now()
    datas_grafico = [(agora - timedelta(days=i)).date() for i in range(6, -1, -1)]
    
    grafico_navios = []
    grafico_ocupacao = []
    grafico_caminhoes = []
    
    # Busca o total de caminhões ativos uma vez só 
    total_caminhoes = db.query(func.count(Caminhao.id)).filter(
        Caminhao.status == StatusCaminhao.ATIVO
    ).scalar() or 0

    for d in datas_grafico:
        # A. Movimentação de Navios
        qtd_chegadas = db.query(func.count(ManifestoCarga.id)).filter(
            cast(ManifestoCarga.data_chegada, Date) == d
        ).scalar() or 0
        
        # AGORA É REAL: Busca pela data_saida
        qtd_saidas = db.query(func.count(ManifestoCarga.id)).filter(
            cast(ManifestoCarga.data_saida, Date) == d
        ).scalar() or 0
        
        grafico_navios.append({
            "data": d.strftime("%d/%m"), 
            "chegadas": qtd_chegadas, 
            "saidas": qtd_saidas
        })
        
        # B. Ocupação (Entradas)
        qtd_entrada = db.query(func.count(Container.id)).filter(
            cast(Container.created_at, Date) == d
        ).scalar() or 0
        
        grafico_ocupacao.append({
            "data": d.strftime("%d/%m"), 
            "total": qtd_entrada
        })
        
        # C. Caminhões
        grafico_caminhoes.append({
            "data": d.strftime("%d/%m"), 
            "total": total_caminhoes
        })

    return {
        "movimentacao_navios": grafico_navios,
        "ocupacao_patio": grafico_ocupacao,
        "caminhoes_ativos": grafico_caminhoes
    }

# ==============================================================================
# 4. ENDPOINT: STATUS E LOGS
# Rota: GET /dashboard/logs
# ==============================================================================
@router.get("/logs")
def get_logs_status(db: Session = Depends(get_db)):
    # 1. Cálculo de Status
    total_containers = db.query(func.count(Container.id)).filter(
        Container.status != StatusContainer.EM_TRANSITO
    ).scalar() or 0
    
    capacidade_patio = 2000
    percentual = (total_containers / capacidade_patio) * 100
    
    if percentual > 90: status_op, nivel_op = "Crítico: Pátio superlotado", 40
    elif percentual > 70: status_op, nivel_op = "Atenção: Alta ocupação", 80
    elif total_containers == 0: status_op, nivel_op = "Sem operações no momento", 100
    else: status_op, nivel_op = "Operação funcionando normalmente", 100

    # 2. Busca de Logs
    logs_lista = []
    
    ultimos_manifestos = db.query(ManifestoCarga).order_by(desc(ManifestoCarga.created_at)).limit(5).all()
    for m in ultimos_manifestos:
        nome_navio = m.navio.nome if m.navio else f"Navio {m.navio_id}"
        logs_lista.append({
            "evento": "Navio Atracado", 
            "descricao": f"Chegada: {nome_navio}", 
            "data_hora": m.created_at
        })

    ultimos_containers = db.query(Container).order_by(desc(Container.created_at)).limit(5).all()
    for c in ultimos_containers:
        logs_lista.append({
            "evento": "Contêiner Recebido", 
            "descricao": f"Entrada: {c.modelo} ({c.status.value})", 
            "data_hora": c.created_at
        })

    logs_lista.sort(key=lambda x: x['data_hora'], reverse=True)
    
    return {
        "status_operacional": {"status": status_op, "nivel": nivel_op},
        "logs": logs_lista[:10]
    }