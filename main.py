from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.data_routes import router as api_router
from app.core.config import settings

app = FastAPI(title="Survey API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(api_router)
