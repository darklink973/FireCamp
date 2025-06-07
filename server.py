import socket
import threading
import time

clients = []
pseudos = {}

def handle_client(client_socket, addr):
    pseudo = client_socket.recv(1024).decode()
    pseudos[client_socket] = pseudo
    Time = time.asctime().split(" ")
    broadcast(f"[+] {pseudo} a rejoint le chat.")
    print(f"[+] {pseudo} a rejoint le chat. -- {time.asctime()}")

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                if(message.decode() == "/list"):
                    print(f"[/] {pseudo} à executé la commande /list: {list(pseudos.values())} -- {time.asctime()}")
                    broadcast(f"[/]: {list(pseudos.values())}")
                else:
                    print(f"{pseudo} : {message.decode()} -- {time.asctime()}")
                    broadcast(f"{Time[4]}, {pseudo} : {message.decode()} ")
            else:
                break
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    broadcast(f"[-] {pseudo} a quitté le chat.")
    print(f"[-] {pseudo} a quitté le chat. -- {time.asctime()}")

def broadcast(message):
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen()
    print("Serveur lancé sur 127.0.0.1:9999")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
