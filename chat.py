import flet as ft
import keyboard



def main(page: ft.Page):
    col_chat = ft.Column()
    messageBox = ft.TextField()

    def send_message(e):
        col_chat.controls.append(ft.Text(value=messageBox.value))
        messageBox.value = ""
        page.update()

    page.add(
        col_chat, ft.Row(controls=[messageBox, ft.ElevatedButton("Send", icon='Send', on_click=send_message)])
    )




ft.app(main)