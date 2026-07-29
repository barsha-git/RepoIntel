from fastapi import FastAPI
from app.api.routes import health, repository, indexing
from app.core.config import settings 

def create_app() -> FastAPI:
    """Create a FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )

    # Include API routes
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(repository.router, prefix="/api/v1", tags=["Repositories"])
    app.include_router(indexing.router, prefix="/api/v1", tags=["indexing"])
    return app

app = create_app()



  