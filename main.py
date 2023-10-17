#VaultTalk
import flet as ft
from flet import *
from cryptography.fernet import Fernet

def main(page: Page):
    ## Window Settings ##
    page.title = "VaultTalk"
    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False
    page.window_maximizable = False
    page.window_resizable = True
    page.window_width = 450
    page.window_height = 600
    page.theme = ft.Theme(color_scheme_seed='blue')

    ## Functions ##
    def themechange(e):
        page.theme = ft.Theme(color_scheme_seed=dd_Theme.value)
        page.update()

    def close_app(e):
        page.window_destroy()



    ## Items ##
    btn_StartSession = ft.ElevatedButton(
        content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="START SESSION", size=20),    
                        ft.Text(value="start a new encrypted chating session", size=10),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
        )
    )
    
    btn_JoinSession = ft.ElevatedButton("Join Session")

    dd_Theme = ft.Dropdown(
        on_change=themechange,
        hint_text="Theme",
        width=125,
        options=[
            ft.dropdown.Option("blue"),
            ft.dropdown.Option("green"),
            ft.dropdown.Option("red"),
            ft.dropdown.Option("purple"),
            ft.dropdown.Option("orange"),
            ft.dropdown.Option("yellow"),
            ft.dropdown.Option("pink"),
        ]
    )

    btn_Close = ft.ElevatedButton("CLOSE",
        icon="close",
        icon_color="red",
        color="red",
        bgcolor="white",
        on_click=close_app,
    )
    
    page.add(btn_StartSession) 
    page.add(btn_JoinSession)
    page.add(dd_Theme)
    page.add(btn_Close)
    page.update()
    pass

if __name__ == "__main__":
        ft.app(target=main)




