from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.infrastructure.database.health import ping_database
from app.infrastructure.database.session import get_db_session


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    @app.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/db", tags=["system"])
    async def database_health_check(
        session: AsyncSession = Depends(get_db_session),
    ) -> dict[str, str]:
        is_connected = await ping_database(session)
        return {"status": "ok" if is_connected else "unavailable"}

    return app


app = create_app()
