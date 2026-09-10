import base64
import socket
import sys
import threading
from typing import NoReturn
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HOST: str = '127.0.0.1'
PORT: int = 5000
BUFFER_SIZE: int = 4096
SALT: bytes = b'pypy_e2ee_network_salt_2026'


def derive_key(passphrase: str) -> bytes:
    """Derives a Fernet key from a user passphrase using PBKDF2."""
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode('utf-8')))


def receive_messages(sock: socket.socket, cipher: Fernet) -> None:
    """Thread function to listen for and decrypt incoming network messages."""
    while True:
        try:
            encrypted_data: bytes = sock.recv(BUFFER_SIZE)
            if not encrypted_data:
                print('\n[!] Connection closed by the server.')
                sys.exit()

            decrypted_msg: str = cipher.decrypt(encrypted_data).decode('utf-8')
            print('\r' + decrypted_msg + '\nYou > ', end='')
        except Exception:
            print('\n[!] Error decrypting message (wrong key or corrupted data).')
            break


def main() -> None:
    username: str = input('Enter your username: ')
    room_key: str = input('Enter room password (E2EE): ')

    key: bytes = derive_key(room_key)
    cipher: Fernet = Fernet(key)

    client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print('[!] Could not connect to the relay server.')
        return

    thread: threading.Thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, cipher),
        daemon=True,
    )
    thread.start()

    print('[*] Connected successfully. E2EE active.\n')

    while True:
        try:
            text: str = input('You > ')
            if text.lower() == '/quit':
                break

            formatted_msg: str = '[' + username + ']: ' + text
            encrypted_payload: bytes = cipher.encrypt(formatted_msg.encode('utf-8'))
            client_socket.sendall(encrypted_payload)
        except (KeyboardInterrupt, EOFError):
            break

    client_socket.close()
    print('\n[*] Connection closed.')


if __name__ == '__main__':
    main()