from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from .server import Server

origins = ["*"]


def create_app(_=None) -> FastAPI:
    app = FastAPI(title="BotAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def exception_handler(request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({"detail": str(exc)}),
        )

    @app.on_event("startup")
    async def startup():
        redis = aioredis.from_url("redis://redis", encoding="utf8",
                                  decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    return Server(app).get_app()