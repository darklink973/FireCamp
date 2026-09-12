import threading

running = threading.Event()

clients = []
pseudos = {}
adresses = {}
groups = {"main_server":[]}
