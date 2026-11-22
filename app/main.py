from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.session import engine
from app.models.entities import Base
from app.services.cache import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _: FastAPI = app
    async with AsyncExitStack() as cleanup:
        cleanup.push_async_callback(engine.dispose)
        cleanup.push_async_callback(close_redis)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield


app = FastAPI(title="AI Resume Analyzer", version="0.1.0", lifespan=lifespan)
app.include_router(router)
__all__: list[str] = ["app"]


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
