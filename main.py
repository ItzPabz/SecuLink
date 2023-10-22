#VaultTalk
import flet as ft
from flet import *
import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import keyboard
        

def main(page: ft.Page) -> None:
    page.title = "VaultTalk"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximizable = False
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 600
    page.theme = ft.Theme(color_scheme_seed=ft.colors.DEEP_PURPLE)
    page.dark_theme

    # INITIAL PAGE
    tx_Header: Text = Text(value='VaultTalk', size=34, width=300, text_align=ft.TextAlign.CENTER)
    tx_tagline: Text = Text(value='Sleek • Fast • Encrpyted', size=16, width=300, text_align=ft.TextAlign.CENTER)
    tf_nickname: TextField = TextField(label='Nickname', text_align=ft.TextAlign.LEFT, width=300)
    btn_StartChat: ElevatedButton = ElevatedButton(text='Start Chat', width=300, disabled=True)

    # CONNECTION PAGE
    tx_Connect: Text = Text(value='Connect to a Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
    tf_ipfield: TextField = TextField(label='Host IP Address', text_align=ft.TextAlign.CENTER, width=300)
    btn_Connect: ElevatedButton = ElevatedButton(text='Connect', width=300, disabled=False)
    tx_Host: Text = Text(value='Become a Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
    btn_Host: ElevatedButton = ElevatedButton(text='Host', width=300)


    # Functions
    def validateFields(e: ControlEvent) -> None:
        if all([tf_nickname.value]):
            btn_StartChat.disabled = False
        else:
            btn_StartChat.disabled = True
        
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
        host_ip_address = socket.gethostbyname(host)
        port = 8765
        server_socket.bind((host, port))
        server_socket.listen(1)


        # ignore plz python cant ref
        def send_button_click(e: ControlEvent) -> None:
            message_info = f'[{tf_nickname.value}]:   {tf_messageHost.value}'
            send_message(message_info)
            tf_messageHost.focus()
        
        keyboard.on_press_key('enter', send_button_click)
            
        # HOST PAGE/VIEW
        tx_HostTitle: Text = Text(value=f'VaultTalk • Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
        lv_chat: ListView = ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        tf_messageHost: TextField = TextField(label='Message', text_align=ft.TextAlign.LEFT, width=250)
        btn_HostSend: IconButton = IconButton(icon='Send', icon_size=50, tooltip='Send Message', icon_color='white', on_click=send_button_click, disabled=False)

        page.clean()
        page.add(
            Row(
                controls=[
                    Column(
                        [
                        tx_HostTitle,
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        tx_HostTitle.value = f'VaultTalk • {host_ip_address}'
        page.add(lv_chat)
        page.add(
            Row([tf_messageHost, btn_HostSend],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        client_socket, addr = server_socket.accept()
        btn_HostSend.disabled = False
        tx_HostTitle.value = f'VaultTalk • Connected'
        page.update()


        host_msg_stat = False
        def send_message(message: str) -> None:
            nonlocal host_msg_stat
            if not host_msg_stat:
                lv_chat.controls.append(ft.Text(value=f'{message}'))
                client_socket.send(message.encode())
                tf_messageHost.value = ''
                host_msg_stat = True
                page.update()
            host_msg_stat = False
    


        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f'Received from client: {data.decode()}')
            lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
            page.update()
            if data.decode() == 'close':
                break
        client_socket.close()
        lv_chat.controls.append(ft.Text(value=f'####### USER HAS DISCONNECTED #######'))
        page.update()

    



    def connect(e: ControlEvent) -> None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = tf_ipfield.value
        port = 8765
        client_socket.connect((host, port))

       # ignore plz python cant ref
        def send_button_click(e: ControlEvent) -> None:
            message_info = f'[{tf_nickname.value}]:   {tf_messageClient.value}'
            send_message(message_info)
            tf_messageClient.focus()

        keyboard.on_press_key('enter', send_button_click)

        # HOST PAGE/VIEW
        tx_HostTitle: Text = Text(value=f'VaultTalk • Client', size=24, width=300, text_align=ft.TextAlign.CENTER)
        lv_chat: ListView = ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        tf_messageClient: TextField = TextField(label='Message', text_align=ft.TextAlign.LEFT, width=250)
        btn_ClientSend: IconButton = IconButton(icon='Send', icon_size=50, tooltip='Send Message', icon_color='white', on_click=send_button_click, disabled=False)

        page.clean()
        page.add(
            Row(
                controls=[
                    Column(
                        [
                        tx_HostTitle,
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        tx_HostTitle.value = f'VaultTalk • Connected'
        page.add(lv_chat)
        page.add(
            Row([tf_messageClient, btn_ClientSend],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        btn_ClientSend.disabled = False
        print(f'Connected to {host}')

        client_msg_stat = False
        def send_message(message: str) -> None:
            nonlocal client_msg_stat
            if not client_msg_stat:
                lv_chat.controls.append(ft.Text(value=f'{message}'))
                client_socket.send(message.encode())
                tf_messageClient.value = ''
                client_msg_stat = True
                page.update()
            client_msg_stat = False
        


        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f'Received from client: {data.decode()}')
            lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
            page.update()


            if data.decode() == 'close':
                break
        client_socket.close()
        lv_chat.controls.append(ft.Text(value=f'####### USER HAS DISCONNECTED #######'))
        page.update()

        



    # Link Functions to UI
    tf_nickname.on_change = validateFields
    btn_StartChat.on_click = createAccount

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
                    btn_StartChat
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


if __name__ == '__main__':
    ft.app(main)