import threading, time
from src.functions import *
from src.variables import *
from handle_client import *

if __name__ == "__main__":
    while True:
        command = input(">>> ")
        #commandes avant le lancement du serveur
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
