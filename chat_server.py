import socket
import select
import sys
import threading
import datetime

# Global variables
clients = {}
chat_rooms = {}


def broadcast(message, room):
    for client in chat_rooms[room]:
        try:
            client.send(message)
        except:
            client.close()
            remove(client, room)


def remove(client, room):
    if client in chat_rooms[room]:
        chat_rooms[room].remove(client)


def client_thread(client_socket, address, name, room):
    try:
        client_socket.send(f"Welcome to the chat room, {name}!\n".encode())

        message = f"{name} has joined the chat.\n"
        broadcast(message.encode(), room)

        while True:
            message = client_socket.recv(2048)
            if message:
                formatted_message = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {name}: {message.decode()}"
                print(formatted_message)
                broadcast(formatted_message.encode(), room)
            else:
                break
    except Exception as e:
        print(e)
    finally:
        client_socket.close()
        remove(client_socket, room)
        message = f"{name} has left the chat.\n"
        broadcast(message.encode(), room)


def create_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(100)
    print(f"Server is running on {ip}:{port}")

    while True:
        client_socket, client_address = server.accept()
        name = client_socket.recv(1024).decode()
        room = client_socket.recv(1024).decode()

        if room not in chat_rooms:
            chat_rooms[room] = []

        chat_rooms[room].append(client_socket)
        clients[client_socket] = (name, room)

        print(f"{name} connected to room {room}")
        client_socket.send(f"Connected to {room} chat room.\n".encode())

        client_handler = threading.Thread(target=client_thread, args=(client_socket, client_address, name, room))
        client_handler.start()


if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print("Correct usage: script, IP address, port number")
        exit()

    IP_address = sys.argv[1]
    Port = int(sys.argv[2])
    create_server(IP_address, Port)
