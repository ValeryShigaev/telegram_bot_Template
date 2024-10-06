from . import auth
from .routes import Routes

__routes__ = Routes(
    routers=(
        auth.router,
    )
)
