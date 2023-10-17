#VaultTalk
import flet as ft
from flet import *
from cryptography.fernet import Fernet
import json, os

def main(page: ft.Page) -> None:
    page.title = "VaultTalk"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximizable = False
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 600
    page.theme = ft.Theme(color_scheme_seed='blue')

    # Setup Login Fields
    tx_Header: Text = Text(value='VaultTalk', size=34, width=300, text_align=ft.TextAlign.CENTER)
    tx_tagline: Text = Text(value='Sleek • Fast • Encrpyted', size=16, width=300, text_align=ft.TextAlign.CENTER)
    tf_nickname: TextField = TextField(label='Nickname', text_align=ft.TextAlign.LEFT, width=300)
    tf_key: TextField = TextField(label='Private Key', text_align=ft.TextAlign.LEFT, width=300, password=True)
    btn_CreateAcct: ElevatedButton = ElevatedButton(text='Create Account', width=300, disabled=True)

    def validateFields(e: ControlEvent) -> None:
        if all([tf_nickname.value, tf_key.value]):
            btn_CreateAcct.disabled = False
        else:
            btn_CreateAcct.disabled = True
        
        page.update()



    def createAccount(e: ControlEvent) -> None:
        json_data = {"nickname": tf_nickname.value, "privateKey": tf_key.value}
        with open('user-info.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        page.clean()
        page.add(
            Row(
                controls=[Text(value=f"Welcome {tf_nickname.value}", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )



    # Link Functions to UI
    tf_nickname.on_change = validateFields
    tf_key.on_change = validateFields
    btn_CreateAcct.on_click = createAccount

    #Renger Page
    if os.path.isfile('user-info.json'):
        page.add(
            Row(
                controls=[Text(value=f"Welcome {tf_nickname.value}", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    else:
        page.add(
            Row(
                controls=[
                    Column(
                        [
                        tx_Header,
                        tx_tagline,
                        tf_nickname, 
                        tf_key,
                        btn_CreateAcct
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )


if __name__ == '__main__':
    ft.app(main)


