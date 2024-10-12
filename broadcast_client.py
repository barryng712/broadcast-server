import socket
import argparse
import threading

HOST='127.0.0.1'
PORT=8801

def send_message(client_socket):
    try:
        while True:
            message = input("")
            client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Client shutting down...")

def receive_message(client_socket):
    while True:
        try:
            message=client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n{message}")
        except:
            print('Connection lost ...')
            client_socket.close()
            break

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Connected to the server. Start chatting!")

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    receive_thread=threading.Thread(target=receive_message, args=(client_socket,))
    send_thread.start()
    receive_thread.start()


if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Broadcast client cli')
    parser.add_argument('command', choices=['connect'])
    args=parser.parse_args()
    if args.command == 'connect':
        connect_to_server()