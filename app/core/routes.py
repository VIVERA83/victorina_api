import typing

if typing.TYPE_CHECKING:
    from core.components import Application


def setup_routes(app: "Application"):
    from victorina.views import victorina_route
    app.include_router(victorina_route)
