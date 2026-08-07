from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, health, repository, indexing
from app.core.config import settings 

def create_app() -> FastAPI:
    """Create a FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(repository.router, prefix="/api/v1", tags=["Repositories"])
    app.include_router(indexing.router, prefix="/api/v1", tags=["indexing"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    return app

app = create_app()



  