import socket, threading, time

running = True

clients = []
pseudos = {}
adresses = {}
groups = {"main_server":[]}

def handle_client(client_socket, addr):
    init_msg = client_socket.recv(1024).decode().split(", ")
    pseudo = get_unique_pseudo(client_socket, init_msg)
    
    if pseudo is None:
        client_socket.close()
        return
    
    pseudos[client_socket] = pseudo
    adresses[pseudo] = addr

    groups["main_server"].append(pseudo)
    broadcast(f"[+] {pseudo} a rejoint le chat.")
    print(f"[+] {pseudo} a rejoint le chat. -- {time.asctime()}")

    while True:
        try:
            message = client_socket.recv(1024)
            
            if message:
                if(message.decode().startswith("/group")):
                    try:
                        arg = message.decode().split(" ")
                        if(arg[1] == "create"):
                            create_group(arg[2])
                        elif(arg[1] == "join"):
                            if(arg[2] in groups):
                                send_to_username(pseudo, "[/] Connexion en cours...")
                                time.sleep(0.5)
                                send_to_username(pseudo, f"[/] Redirection de: {search_names_in_groups(pseudo)} vers: {arg[2]} reussie !")
                                move_users_to_groups(pseudo, arg[2])
                            else:
                                send_to_username(pseudo, "[/] Nom du groupe invalide !")
                    except:
                        send_to_username(pseudo, "[/] Ne pas utiliser d'espaces dans le nom du groupe merci !")
                        print("Erreur: /group")
                elif(message.decode().startswith("/msg")):
                    try:
                        arg = message.decode().split(" ")
                        Message = message.decode().replace("/msg " + arg[1], f"<de:{arg[1]}>:")
                        send_to_username(arg[1], Message)
                    except:
                        print("Erreur: /msg")
                        pass
                elif(message.decode() == "/list"):
                    print(f"[/] {pseudo} à executé la commande /list: {str(groups[search_names_in_groups(pseudo)])} -- {time.asctime()}")
                    # broadcast(f"[/]: {list(pseudos.values())}")
                    send_to_username(pseudo, f"[/] {search_names_in_groups(pseudo)}: " + str(groups[search_names_in_groups(pseudo)]))
                    print(adresses)
                elif(message.decode() == "/quit"):
                    groups[search_names_in_groups(pseudo)].remove(pseudo)
                    del adresses[pseudo]
                    del pseudos[client_socket]
                    break
                else:
                    send_to_group(search_names_in_groups(pseudo), message.decode(), pseudo)
            else:
                break
        except:
            break
    
    client_socket.close()
    clients.remove(client_socket)
    
    broadcast(f"[-] {pseudo} a quitté le chat.")
    print(f"[-] {pseudo} a quitté le chat. -- {time.asctime()}")

def get_unique_pseudo(client_socket, msg):
    pseudo = msg[0]
    if not pseudo:
        return None
    if len(pseudo) <= 3:
        client_socket.sendall(
            "Votre pseudo est trop court ! (min 3 caractères)".encode()
        )
        return None
    if len(pseudo) >= 12:
        client_socket.sendall(
            "Votre pseudo est trop long ! (max 12 caractères)".encode()
        )
        return None
    if pseudo.startswith("/"):
        client_socket.sendall(
            "Votre pseudo ne peut pas commencer par '/'."
            .encode()
        )
        return None
    if " " in pseudo:
        client_socket.sendall(
            "Votre pseudo ne doit pas contenir d'espaces.\n"
            .encode()
        )
        return None
    if is_pseudo_taken(pseudo):
        client_socket.sendall(
            "Ce pseudo est déjà utilisé. Veuillez en choisir un autre."
            .encode()
        )
        return None
    return pseudo

def is_pseudo_taken(pseudo):
    return pseudo in pseudos.values()

def create_group(nom):
    if not nom in groups:
        val = {nom: []}
        groups.update(val)

def send_to_group(group, message, username):
    try:
        Message = f"<{username}>: {message}"
        for key, value in groups.items():
            for val in value:
                if(key == group):
                    send_to_username(val, Message)
    except:
        print("Erreur fonction: send_to_group")
        return

def move_users_to_groups(username, group):
    try:
        groups[search_names_in_groups(username)].remove(username)
        groups[group].append(username)
    except:
        print("Erreur fonction: move_users_to_groups")
        return

def search_names_in_groups(username):
    try:
        for key, value in groups.items():
            for val in value:
                if username == val:
                    return key
    except:
        print("Erreur fonction: search_names_in_groups, utilisateur introuvable ?")
        pass

def send_to_username(username, message):
    ip_and_port = adresses[username]
    # print(ip_and_port, adresses, clients, username)
    try:
        for client in clients:
            if(client.getpeername() == ip_and_port):
                # print(message, client)
                client.sendto(message.encode("utf-8"), (ip_and_port[0], ip_and_port[1]))
    except:
        print("Erreur fonction: send_to_username")
        return

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

    while running == True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
    if running == False:
        server.

if __name__ == "__main__":
    while True:
        command = input(">>> ")
        #threading.Thread(target=start_server).start
        # if(command == "start"):
        #     t1 = threading.Thread(target=start_server)
        #     t1.start()
        #     time.sleep(0.5)
        #     pass
        match command:
            case "start":
                t1 = threading.Thread(target=start_server)
                t1.start()
                time.sleep(0.5)
            case "list":
                print(groups)
            case "help":
                print('Voici les commandes: \n -"start", \n -"list"') # A terminer pls
            case "stop":
                broadcast("Serveur éteint.")
                server.unbind()
                running = False