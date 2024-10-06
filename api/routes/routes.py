from dataclasses import dataclass
from fastapi import APIRouter, FastAPI
from typing import Tuple

main_router = APIRouter(
    prefix=''
)


@dataclass(frozen=True)
class Routes:
    routers: Tuple

    def register_routes(self, app: FastAPI):
        for router in self.routers:
            main_router.include_router(router)
        app.include_router(main_router)