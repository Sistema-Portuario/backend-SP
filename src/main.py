from fastapi import FastAPI
from src.routes.usuario_routes import router as usuario_router
from src.routes.cargo_routes import router as cargo_router

app = FastAPI()

app.include_router(usuario_router)
app.include_router(cargo_router)
