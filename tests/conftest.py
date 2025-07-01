import flet as ft

import flet_easy as fs

app = fs.FletEasy(
    route_init="/home",
)


@app.page("/home", title="Index - Home")
async def index_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Men", size=40),
            ft.ElevatedButton(
                "Go to Test",
                on_click=data.go(f"{data.route_prefix}/test/10/user/dxs"),
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@app.page("/testy", title="Testy")
def testy_page(data: fs.Datasy, id: int, name: str):
    return ft.View(
        controls=[
            ft.Text(f"Test {id} | {name}"),
            ft.Text(f"Test Id is: {id}"),
            ft.ElevatedButton("Go to Home", on_click=data.go(data.route_init)),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
