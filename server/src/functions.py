from server.src.variables import *
import socket
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

def create_group(nom, username):
    if not nom in groups:
        val = {nom: []}
        groups.update(val)
        send_to_username(username, f"Groupe <{nom}> créé")
    else:send_to_username(username, "Nom de groupe déjà attribué")

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
