from fastapi import FastAPI
from src.routes.usuario_routes import router as usuario_router
from src.routes.cargo_routes import router as cargo_router
from src.routes.navio_routes import router as navio_router
from src.routes.container_routes import router as container_router
from src.routes.setor_routes import router as setor_router
from src.routes.caminhao_routes import router as caminhao_router
from src.controllers.dashboard_controller import router as dashboard_router

app = FastAPI()

app.include_router(usuario_router)
app.include_router(cargo_router)
app.include_router(navio_router)
app.include_router(container_router)
app.include_router(setor_router)
app.include_router(caminhao_router)
app.include_router(dashboard_router)