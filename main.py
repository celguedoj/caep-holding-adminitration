from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.infrastructure.database.health import ping_database
from app.infrastructure.database.init_db import create_database_tables
from app.infrastructure.database.session import get_db_session
from app.presentation.routers import auth, companies, departments, employees, products


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await create_database_tables()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
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

    app.include_router(auth.router)
    app.include_router(companies.router)
    app.include_router(companies.protected_router)
    app.include_router(departments.router)
    app.include_router(employees.router)
    app.include_router(products.router)

    return app


app = create_app()
