#VaultTalk
import flet as ft
from flet import *
from cryptography.fernet import Fernet



def main(page: Page):
    page.title = "VaultTalk"

    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False
    page.window_maximizable = False
    page.window_resizable = True
    page.window_width = 450
    page.window_height = 600





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
    
    page.add(btn_StartSession)
    btn_JoinSession = ft.ElevatedButton("Join Session")
    page.add(btn_JoinSession)    


    page.update()
    pass

if __name__ == "__main__":
        ft.app(target=main)




