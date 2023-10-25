#All the libararies used within the project
import flet as ft
from flet import *
import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import keyboard
        
# Main fucntion, contains whole application
def main(page: ft.Page) -> None:
    #Default Page Settings
    page.title = "VaultTalk • Encrypted Chat"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_maximizable = False
    page.window_resizable = False
    page.window_width = 450
    page.window_height = 600
    page.theme = ft.Theme(color_scheme_seed=ft.colors.DEEP_PURPLE)
    page.theme_mode = ft.ThemeMode.DARK

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


    ###########################################
    ################ Functions ################
    ###########################################
    # Function to make sure a username is entered before connecting
    def validateFields(e: ControlEvent) -> None:
        if all([tf_nickname.value]):
            btn_StartChat.disabled = False
        else:
            btn_StartChat.disabled = True
        
        page.update()

    # Function to create the account and load the connection option page
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
    
    # Function to start the server and load the host page
    def start_server(e: ControlEvent) -> None:
        # Socket Information
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        host_ip_address = socket.gethostbyname(host)
        port = 8765
        server_socket.bind((host, port))
        server_socket.listen(1)

        # Encryption Information
        host_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        host_private_key_pem = host_private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        host_public_key = host_private_key.public_key()
        host_public_key_pem = host_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Function to sent message either encrypted or not 
        host_msg_stat = False
        def send_message(message: str) -> None:
            nonlocal host_msg_stat
            if not host_msg_stat:
                # Checks encryption switch
                if sw_EncryptMsg.value == False:
                    # If encryption is off (sends message normally)
                    lv_chat.controls.append(ft.Text(value=f'{message.decode()}'))
                    client_socket.send(message)
                    tf_messageHost.value = ''
                    host_msg_stat = True
                    page.update()
                else:
                    # If encryption is on (encrypts message and sends it)
                    lv_chat.controls.append(ft.Text(value=f'{message.decode()}'))
                    try:
                        client_pub_key = serialization.load_pem_public_key(firstmsg_key)
                        encrypted_msg = client_pub_key.encrypt(
                            message.decode().encode(), 
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                algorithm=hashes.SHA256(), 
                                label=None
                            )
                        )
                        client_socket.send(encrypted_msg)
                        tf_messageHost.value = ''
                        client_msg_stat = True
                        page.update()
                    except ValueError:
                    # In the event of an error, the message is sent normally (Should not happen but this is a failsafe)
                        print('Invalid public key format')
            # Resets the message status (so it wont spam the chat)
            host_msg_stat = False

        #Function to send message when enter is pressed
        def send_button_click(e: ControlEvent) -> None:
            if tf_messageHost.value == '':
                return False
            else:
                message_info = f'[{tf_nickname.value}]:   {tf_messageHost.value}'
                send_message(message_info.encode())
                tf_messageHost.focus()
        keyboard.on_press_key('enter', send_button_click)
            
        # Host Chat View/Layout
        tx_HostTitle: Text = Text(value=f'VaultTalk • Host', size=24, width=300, text_align=ft.TextAlign.CENTER)
        lv_chat: ListView = ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        tf_messageHost: TextField = TextField(label='Message', text_align=ft.TextAlign.LEFT, width=250)
        btn_HostSend: IconButton = IconButton(icon='Send', icon_size=50, tooltip='Send Message', icon_color='white', on_click=send_button_click, disabled=False)
        sw_EncryptMsg: Switch = Switch(label='', value=False, width=50, tooltip='Encrypt Messages', active_color='green', inactive_thumb_color='red')
        page.clean()
        page.add(
            Row(
                controls=[
                    Column(
                        [
                        tx_HostTitle
                        ]
                    )
                ],
                
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        tx_HostTitle.value = f'VaultTalk • {host_ip_address}'
        page.add(lv_chat)
        page.add(
            Row([tf_messageHost, btn_HostSend, sw_EncryptMsg],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        # Waits for a client connection. Once connected, sends the public key and recieves the client's public key
        client_socket, addr = server_socket.accept()
        client_socket.send(host_public_key_pem)
        firstmsg_key = client_socket.recv(1024)
        btn_HostSend.disabled = False
        tx_HostTitle.value = f'VaultTalk • Connected'
        page.update()

        # Recieves messages from the client and displays them in the chat
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                if data == firstmsg_key:
                    # Prevents the first message (Public Key) from being displayed in the chat itself.
                    continue
                if sw_EncryptMsg.value == False:
                    # Checks encryption switch and displays message accordingly
                    try:
                        lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
                        page.update()
                    except UnicodeDecodeError:
                        lv_chat.controls.append(ft.Text(value=f'{data}'))
                        page.update()
                else:
                    # Decrypts message and displays it in the chat
                    try:
                        self_private_key = serialization.load_pem_private_key(host_private_key_pem, password=None)
                        decrypted_msg = self_private_key.decrypt(
                            data,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        lv_chat.controls.append(ft.Text(value=f'{decrypted_msg.decode()}'))
                        page.update()
                    except ValueError:
                        # Handles errors (Used for when a an unencrypted message is sent to encrypted chat)
                        lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
                        page.update()
            except ConnectionResetError:
                #Ends chat when host disconnects
                lv_chat.controls.append(ft.Text(value=f'##### CHAT ENDED #####'))
                btn_HostSend.disabled = True
                sw_EncryptMsg.disabled = True
                tf_messageHost.disabled = True
                tx_HostTitle.value = 'VaultTalk • Disconnected'
                page.update()
                break
        client_socket.close()

    # Connect to a host and load the client page
    def connect(e: ControlEvent) -> None:
        # Socket Information
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = tf_ipfield.value
        port = 8765
        client_socket.connect((host, port))

        # Encryption Information
        client_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        client_private_key_pem = client_private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        client_public_key = client_private_key.public_key()
        client_public_key_pem = client_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Function to send message either encrypted or not
        client_msg_stat = False
        def send_message(message: str) -> None:
            nonlocal client_msg_stat
            if not client_msg_stat:
                if sw_EncryptMsg.value == False:
                    # If encryption is off (sends message normally)
                    lv_chat.controls.append(ft.Text(value=f'{message.decode()}'))
                    client_socket.send(message)
                    tf_messageClient.value = ''
                    client_msg_stat = True
                    page.update()
                else:
                    # If encryption is on (encrypts message and sends it)
                    lv_chat.controls.append(ft.Text(value=f'{message.decode()}'))
                    try:
                        client_pub_key = serialization.load_pem_public_key(firstmsg_key)
                        encrypted_msg = client_pub_key.encrypt(
                            message.decode().encode(), 
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                algorithm=hashes.SHA256(), 
                                label=None
                            )
                        )
                        client_socket.send(encrypted_msg)
                        tf_messageClient.value = ''
                        client_msg_stat = True
                        page.update()
                    except ValueError:
                        # In the event of an error (Should not happen but this is a failsafe)
                        print('Invalid public key format')
            # Resets the message status (so it wont spam the chat)
            client_msg_stat = False

        # Function to send message when enter is pressed
        def send_button_click(e: ControlEvent) -> None:
            if tf_messageClient.value == '':
                return False
            else:
                message_info = f'[{tf_nickname.value}]:   {tf_messageClient.value}'
                send_message(message_info.encode())
                tf_messageClient.focus()
        keyboard.on_press_key('enter', send_button_click)

        # Chat View/Layout
        tx_HostTitle: Text = Text(value=f'VaultTalk • Client', size=24, width=300, text_align=ft.TextAlign.CENTER)
        lv_chat: ListView = ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        tf_messageClient: TextField = TextField(label='Message', text_align=ft.TextAlign.LEFT, width=250)
        btn_ClientSend: IconButton = IconButton(icon='Send', icon_size=50, tooltip='Send Message', on_click=send_button_click, disabled=False)
        sw_EncryptMsg: Switch = Switch(label='', value=False, width=50, tooltip='Encrypt Messages', active_color='green', inactive_thumb_color='red')
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
            Row([tf_messageClient, btn_ClientSend, sw_EncryptMsg],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        btn_ClientSend.disabled = False

        # Sends the public key and recieves the host's public key
        firstmsg_key = client_socket.recv(1024)
        client_socket.send(client_public_key_pem)

        # Recieves messages from the host and displays them in the chat
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                if data == firstmsg_key:
                    continue
                if sw_EncryptMsg.value == False:
                    try:
                        lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
                        
                        page.update()
                    except UnicodeDecodeError:
                        lv_chat.controls.append(ft.Text(value=f'{data}'))
                        page.update()
                else:
                    try:
                        self_private_key = serialization.load_pem_private_key(client_private_key_pem, password=None)
                        decrypted_msg = self_private_key.decrypt(
                            data,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        lv_chat.controls.append(ft.Text(value=f'{decrypted_msg.decode()}'))
                        
                        page.update()
                    except ValueError:
                        lv_chat.controls.append(ft.Text(value=f'{data.decode()}'))
                        
                        page.update()
            except ConnectionResetError:
                #Ends chat when host disconnects
                lv_chat.controls.append(ft.Text(value=f'##### CHAT ENDED #####'))
                btn_ClientSend.disabled = True
                tf_messageClient.disabled = True
                sw_EncryptMsg.disabled = True
                tx_HostTitle.value = 'VaultTalk • Disconnected'
                page.update()
                break
        client_socket.close()

    # Link Functions to UI Elements
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

# Launches the main function
if __name__ == '__main__':
    ft.app(main)