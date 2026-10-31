from src.variables import *

def get_unique_pseudo(client_socket, msg):
    if not msg[0]:
        return None
    if len(msg[0]) <= 3:
        client_socket.sendall(
            "Votre pseudo est trop court ! (min 3 caractères)".encode()
        )
        return None
    if len(msg[0]) >= 12:
        client_socket.sendall(
            "Votre pseudo est trop long ! (max 12 caractères)".encode()
        )
        return None
    if msg[0].startswith("/"):
        client_socket.sendall(
            "Votre pseudo ne peut pas commencer par '/'."
            .encode()
        )
        return None
    if " " in msg[0]:
        client_socket.sendall(
            "Votre pseudo ne doit pas contenir d'espaces.\n"
            .encode()
        )
        return None
    if is_pseudo_taken(msg[0]):
        client_socket.sendall(
            "Ce pseudo est déjà utilisé. Veuillez en choisir un autre."
            .encode()
        )
        return None
    return msg[0]

def is_pseudo_taken(pseudo):
    return pseudo in pseudos.values()

def create_group(nom, username):
    if not nom in groups:
        groups.update({nom: []})
        send_to_username(username, f"Groupe {nom} créé")
    else:
        send_to_username(username, "Nom de groupe déjà attribué")
    
def delete_group(nom, username):
    if nom in groups:
        groups.pop(nom)
        send_to_username(username, f"Groupe {nom} supprimé")
    else:
        send_to_username(username, f"Le groupe {nom} n'existe pas")

def send_to_group(group, message, username):
    try:
        for key, value in groups.items():
            for val in value:
                if(key == group):
                    send_to_username(val, f"<{username}>: {message}")
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
    try:
        for client in clients:
            if(client.getpeername() == adresses[username]):
                client.sendto(message.encode("utf-8"), (adresses[username][0], adresses[username][1]))
    except:
        print("Erreur fonction: send_to_username")
        return

def broadcast(message):
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            client.close()
