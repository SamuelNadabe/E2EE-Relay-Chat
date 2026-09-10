import socket
import threading
from typing import List, Tuple

HOST: str = '127.0.0.1'
PORT: int = 5000
BUFFER_SIZE: int = 4096

clients: List[socket.socket] = []


def broadcast(message: bytes, sender_socket: socket.socket) -> None:
    """Forwards encrypted payload to all connected clients except sender."""
    client: socket.socket
    for client in clients[:]:
        if client != sender_socket:
            try:
                client.sendall(message)
            except OSError:
                if client in clients:
                    clients.remove(client)


def handle_client(client_socket: socket.socket, addr: Tuple[str, int]) -> None:
    """Handles communications with a single client."""
    print('[+] Client connected: ' + str(addr))
    while True:
        try:
            message: bytes = client_socket.recv(BUFFER_SIZE)
            if not message:
                break
            broadcast(message, client_socket)
        except ConnectionResetError:
            break

    print('[-] Client disconnected: ' + str(addr))
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()


def main() -> None:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print('[*] Relay Server active on ' + HOST + ':' + str(PORT) + ' (Zero-Knowledge)')

    while True:
        client_socket: socket.socket
        addr: Tuple[str, int]
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)

        thread: threading.Thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr),
            daemon=True,
        )
        thread.start()


if __name__ == '__main__':
    main()