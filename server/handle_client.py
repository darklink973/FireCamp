import server.src.functions as functions
from server.src.variables import *
import time, socket

def handle_client(client_socket, addr):
    init_msg = client_socket.recv(1024).decode().split(", ")
    pseudo = functions.get_unique_pseudo(client_socket, init_msg)
    
    if pseudo is None:
        client_socket.close()
        return
    
    pseudos[client_socket] = pseudo
    adresses[pseudo] = addr

    groups["main_server"].append(pseudo)
    functions.broadcast(f"[+] {pseudo} a rejoint le chat.")
    print(f"[+] {pseudo} a rejoint le chat. -- {time.asctime()}")

    while True:
        try:
            message = client_socket.recv(1024)
            
            if message:
                if(message.decode().startswith("/group")):
                    try:
                        arg = message.decode().split(" ")
                        if(arg[1] == "create"):
                            functions.create_group(arg[2], pseudo)
                        elif(arg[1] == "join"):
                            if(arg[2] in groups):
                                functions.send_to_username(pseudo, "[/] Connexion en cours...")
                                time.sleep(0.5)
                                functions.send_to_username(pseudo, f"[/] Redirection de: {functions.search_names_in_groups(pseudo)} vers: {arg[2]} reussie !")
                                functions.move_users_to_groups(pseudo, arg[2])
                            else:
                                functions.send_to_username(pseudo, "[/] Nom du groupe invalide !")
                    except:
                        functions.send_to_username(pseudo, "[/] Ne pas utiliser d'espaces dans le nom du groupe merci !")
                        print("Erreur: /group")
                elif(message.decode().startswith("/msg")):
                    try:
                        arg = message.decode().split(" ")
                        Message = message.decode().replace("/msg " + arg[1], f"<de:{arg[1]}>:")
                        functions.send_to_username(arg[1], Message)
                    except:
                        print("Erreur: /msg")
                        pass
                elif(message.decode() == "/list"):
                    print(f"[/] {pseudo} à executé la commande /list: {str(groups[functions.search_names_in_groups(pseudo)])} -- {time.asctime()}")
                    # broadcast(f"[/]: {list(pseudos.values())}")
                    functions.send_to_username(pseudo, f"[/] {functions.search_names_in_groups(pseudo)}: " + str(groups[functions.search_names_in_groups(pseudo)]))
                    print(adresses)
                else:
                    functions.send_to_group(functions.search_names_in_groups(pseudo), message.decode(), pseudo)
            else:
                break
        except:
            break
        
    groups[functions.search_names_in_groups(pseudo)].remove(pseudo)
    del adresses[pseudo]
    del pseudos[client_socket]
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)
    
    functions.broadcast(f"[-] {pseudo} a quitté le chat.")
    print(f"[-] {pseudo} a quitté le chat. -- {time.asctime()}")
    
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
