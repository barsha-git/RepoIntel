from fastapi import FastAPI
from app.api.routes import health
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

    return app

app = create_app()



  