import flet as ft

import flet_easy as fs

login = fs.AddPagesy()


@login.page("/login", title="Login")
async def login_request(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Login"),
            ft.TextField(),
            ft.Button(text="click", on_click=data.go("/")),
        ],
        appbar=ft.AppBar(
            leading=None,
            title=ft.Text("app"),
        ),
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@login.page("/")
async def f(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Index"),
            ft.TextField(),
            ft.Button(text="click", on_click=data.go("/login")),
            ft.Button(text="click", on_click=data.go("/here")),
        ],
        appbar=ft.AppBar(leading=None),
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@login.page("/here")
async def f(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Here"),
            ft.TextField(),
            ft.Button(text="click", on_click=data.go("/login")),
            ft.Button(text="click", on_click=data.go("/")),
        ],
        appbar=ft.AppBar(leading=None),
        vertical_alignment="center",
        horizontal_alignment="center",
    )
