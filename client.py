import socket, os, threading, hashlib
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Configuration
FONT = ("Cascadia Code", 11)
pathDir = os.path.join('C:\\', 'Users', os.getlogin(), 'FireCamp Chat')
pathFile = os.path.join('C:\\', 'Users', os.getlogin(), 'FireCamp Chat', "ipTemp.txt")
# toast = ToastNotifier() deprecated (from win10toast)

print("Créé par Zenith et Darkvox")

# Thèmes
THEMES = {
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "entry_bg": "#f0f0f0",
        "text_bg": "#ffffff",
        "button_bg": "#e0e0e0"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#d4d4d4",
        "entry_bg": "#2d2d2d",
        "text_bg": "#252526",
        "button_bg": "#3c3c3c"
    }
}

class ChatClient:
    
    def __init__(self, master):
        # check si le fichier existe, si non on le crée, si oui on le lis
        if not os.path.exists(pathDir):
            os.mkdir(pathDir)
        self.ip_temp_file_read(0)
        self.master = master
        self.master.title("Client Chat")
        self.master.option_add("*Font", FONT)
        self.current_theme = "light"

        self.pseudo = simpledialog.askstring("Pseudo", "Entrez votre pseudo:", initialvalue=self.ip_temp_file_read(0), parent=self.master)
        if not self.pseudo:
            messagebox.showerror("Erreur", "Pseudo requis !")
            master.destroy()
            return
        
        self.HOST = simpledialog.askstring("IP", "Entrez l'IP du serveur:", initialvalue=self.ip_temp_file_read(1), parent=self.master)
        if not self.HOST:
            messagebox.showerror("Erreur", "IP requise !")
            master.destroy()
            return
        
        self.PORT = simpledialog.askinteger("Port", "Entrez le port du serveur:", initialvalue=self.ip_temp_file_read(2), parent=self.master)
        if not self.PORT:
            messagebox.showerror("Erreur", "Port requis !")
            master.destroy()
            return

        # Layout principal
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=5, pady=5, anchor="nw")

        # Zone d'affichage des messages
        self.chat_display = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, state='disabled', width=60, height=20, font=FONT)
        self.chat_display.grid(row=0, column=0, columnspan=3, sticky="nw")
        
        # Zone d'afficheage des groupes
        #self.chat_display = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, state='disabled', width=60, height=20, font=FONT)
        #self.chat_display.grid(row=0, column=0, columnspan=3, sticky="nw")

        # Entrée message
        self.message_entry = tk.Entry(self.main_frame, width=40, font=FONT)
        self.message_entry.grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.message_entry.bind("<Return>", self.send_message)

        # Bouton envoyer
        self.send_button = tk.Button(self.main_frame, text="Envoyer", command=self.send_message, font=FONT, height=1)
        self.send_button.grid(row=1, column=1, sticky="w", padx=(5, 0), pady=(5, 0))

        # Boutons thème
        self.theme_frame = tk.Frame(self.main_frame)
        self.theme_frame.grid(row=1, column=2, sticky="e", padx=(5, 0))

        self.dark_button = tk.Button(self.theme_frame, text="🌙 Sombre", command=self.set_dark_theme, font=FONT, height=1)
        self.dark_button.grid(row=2, column=1, padx=2)

        self.light_button = tk.Button(self.theme_frame, text="🔆 Clair", command=self.set_light_theme, font=FONT, height=1, state=tk.DISABLED)
        self.light_button.grid(row=0, column=1, padx=2, pady=5)

        # Sauvegarde des identifiants
        self.ip_temp_file_write()

        self.start_connection()
        
    def start_connection(self):
        # Clear le screen
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0)
        self.chat_display.config(state="disabled")
        # Connexion socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((self.HOST, self.PORT))
        except Exception as e:
            messagebox.showerror("Erreur de connexion", str(e))
            self.master.destroy()
            return
        self.client_socket.sendall(self.pseudo.encode())
        self.running = True
    
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.apply_theme()

    # def notif(self, message):
    #     toast.show_toast(
    #         "Notification",
    #         message,
    #         duration = 3,
    #         threaded = True,
    #     )
    # deprecated

    def ip_temp_file_read(self, ip_or_port):
        try:
            with open(pathFile, "r") as file:
                text = file.read()
                ip = text.split(":")
                if(ip_or_port == 0):
                    return ip[0]
                if(ip_or_port == 1):
                    return ip[1]
                if(ip_or_port == 2):
                    return ip[2]
        except:
            open(pathFile, "x")
            with open(pathFile, "w") as file:
                file.write(str("username:0.0.0.0:0"))
                self.ip_temp_file_read(ip_or_port)

    def ip_temp_file_write(self):
        with open(pathFile, "w") as file:
            file.write(self.pseudo + ":" + str(self.HOST) + ":" + str(self.PORT))

    def apply_theme(self):
        t = THEMES[self.current_theme]
        self.master.configure(bg=t["bg"])
        self.main_frame.configure(bg=t["bg"])
        self.theme_frame.configure(bg=t["bg"])

        # Appliquer le thème aux widgets
        self.chat_display.configure(
            bg=t["text_bg"], fg=t["fg"], insertbackground=t["fg"]
        )
        self.message_entry.configure(
            bg=t["entry_bg"], fg=t["fg"], insertbackground=t["fg"]
        )

        for button in [self.send_button, self.dark_button, self.light_button]:
            button.configure(
                bg=t["button_bg"], fg=t["fg"], activebackground=t["entry_bg"]
            )

    def set_dark_theme(self):
        self.current_theme = "dark"
        self.apply_theme()
        self.dark_button.config(state=tk.DISABLED)
        self.light_button.config(state=tk.NORMAL)

    def set_light_theme(self):
        self.current_theme = "light"
        self.apply_theme()
        self.light_button.config(state=tk.DISABLED)
        self.dark_button.config(state=tk.NORMAL)

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                self.display_message(message)
                if not message:
                    break
            except ConnectionResetError:
                self.running = False
                break
        self.display_message("Erreur de connexion au serveur")
                
    def send_message(self, event=None):
        message = self.message_entry.get()
        
        if message:
            try:
                self.client_socket.sendall(message.encode())
                self.message_entry.delete(0, tk.END)
            except ConnectionAbortedError:
                self.start_connection()

    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

    def on_expected_closing(self):
        self.running = False
        
        try:
            self.client_socket.close()
        except:
            print("error on closing")
            
        self.master.destroy()

# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_expected_closing)
    root.mainloop()

