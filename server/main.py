import threading, time
from server.src.functions import *
from server.src.variables import *
from handle_client import *

if __name__ == "__main__":
    while True:
        command = input(">>> ")
        match command:
            case "start":
                t1 = threading.Thread(target=start_server)
                t1.start()
                time.sleep(0.5)
            case "list":
                print(groups)
            case "help":
                print('Voici les commandes: \n -"start", \n -"list"')
            case "stop":
                broadcast("Serveur éteint.")
                running.clear()
