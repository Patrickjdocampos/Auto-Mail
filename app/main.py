from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.routes.analysis import router as analysis_router
from app.routes.health import router as health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router, tags=["Health"])
app.include_router(analysis_router, tags=["Analysis"])