#VaultTalk
import flet as ft
from flet import *
import socket
        

def main(page: ft.Page) -> None:
    page.title = "VaultTalk"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximizable = False
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 600
    page.theme = ft.Theme(color_scheme_seed='blue')

    # Setup Login Fields
    # INITIAL PAGE
    tx_Header: Text = Text(value='VaultTalk', size=34, width=300, text_align=ft.TextAlign.CENTER)
    tx_tagline: Text = Text(value='Sleek • Fast • Encrpyted', size=16, width=300, text_align=ft.TextAlign.CENTER)
    tf_nickname: TextField = TextField(label='Nickname', text_align=ft.TextAlign.LEFT, width=300)
    tf_key: TextField = TextField(label='Private Key', text_align=ft.TextAlign.LEFT, width=300, password=True)
    btn_CreateAcct: ElevatedButton = ElevatedButton(text='Create Account', width=300, disabled=True)

    # CONNECTION PAGE
    tx_Connect: Text = Text(value='Connect to a Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
    tf_ipfield: TextField = TextField(label='Host IP Address', text_align=ft.TextAlign.CENTER, width=300)
    btn_Connect: ElevatedButton = ElevatedButton(text='Connect', width=300, disabled=False)
    tx_Host: Text = Text(value='Become a Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
    btn_Host: ElevatedButton = ElevatedButton(text='Host', width=300)





    # Functions
    def validateFields(e: ControlEvent) -> None:
        if all([tf_nickname.value, tf_key.value]):
            btn_CreateAcct.disabled = False
        else:
            btn_CreateAcct.disabled = True
        
        page.update()

    def createAccount(e: ControlEvent) -> None:
        page.clean()
        page.add(
        Row(
            controls=[
                Column(
                    [
                    tx_Header,
                    tx_Connect,
                    tf_ipfield,
                    btn_Connect,
                    tx_Host,
                    btn_Host,
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
        
    def start_server(e: ControlEvent) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 8765
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Waiting for connection...")
        client_socket, addr = server_socket.accept()
        print("Connection from " + str(addr))
        data = client_socket.recv(1024)
        print("Received: " + str(data))
        client_socket.close()

    def connect(e: ControlEvent) -> None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = tf_ipfield.value
        port = 8765
        client_socket.connect((host, port))
        message = "Hello Server!"
        client_socket.send(message.encode())
        client_socket.close()



    # Link Functions to UI
    tf_nickname.on_change = validateFields
    tf_key.on_change = validateFields
    btn_CreateAcct.on_click = createAccount

    btn_Host.on_click = start_server
    btn_Connect.on_click = connect

    #Renger Page
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


