from pathlib import Path

import flet.fastapi as flet_fastapi

import flet_easy as fs

app = fs.FletEasy(
    route_init="/",
    path_views=Path(__file__).parent / "views",
)

fastapi = flet_fastapi.FastAPI()


fastapi.mount("/", flet_fastapi.app(app.get_app()))
