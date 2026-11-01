import threading, time
from src.functions import *
from src.variables import *
from handle_client import *

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen()
    server.settimeout(1)
    running.set()
    print("Serveur lancé sur 127.0.0.1:9999")

    while running.is_set():
        try:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            threading.Thread(
                target=handle_client,
                args=(client_socket, addr),
                daemon=True
            ).start()

        except socket.timeout:
            continue
    print("Arrêt du serveur...")
    
    for client in clients:
        try:
            client.shutdown(socket.SHUT_RDWR)
        except:
            pass
        client.close()
    clients.clear()
    server.close()
    print("Serveur arrêté.")


if __name__ == "__main__":
    while True:
        command = input(">>> ")
        # commandes avant le lancement du serveur
        match command:
            case "start":
                t1 = threading.Thread(target=start_server)
                t1.start()
                time.sleep(0.5)
            case "list":
                print(groups)
            case "help":
                print('Voici les commandes: \n -"start", \n -"list", \n -"stop"')
            case "stop":
                broadcast("Serveur éteint.")
                running.clear()

