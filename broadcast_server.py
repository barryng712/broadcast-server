import socket
import threading
import argparse
import sys

HOST='127.0.0.1'
PORT=8801
clients =[]
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    to_remove = []  # List to track clients to remove
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Error sending message: {e}")
                    to_remove.append(client)  # Mark for removal
    # Remove clients outside the lock to avoid modifying the list while iterating
    with clients_lock:
        for client in to_remove:
            if client in clients:  # Check if still in the list
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except (ConnectionResetError, ConnectionAbortedError):
            break
    with clients_lock:
        clients.remove(client_socket)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
    except OSError as e:
        print(f"Error binding to port: {e}")
        sys.exit(1)

    print("Server started, waiting for clients to connect ...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address[1]} connected.")
        with clients_lock:
            clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    parser= argparse.ArgumentParser(description='Broadcast Server CLI')
    parser.add_argument('command', choices=['start'])
    args = parser.parse_args()
    if args.command == 'start':
        start_server()
