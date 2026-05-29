import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
import json
import os
from tkinter import filedialog
from plyer import notification

HOST = '127.0.0.1'
PORT = 5555

EMOJIS = {
    ":smile:": "😊",
    ":heart:": "❤️",
    ":fire:": "🔥",
    ":thumbs:": "👍",
    ":party:": "🎉",
    ":cool:": "😎"
}


class ChatClient:

    def show_notification(self, sender, message):
        notification.notify(
        title=f"New message from {sender}",
        message=message,
        app_name="Chat App",
        timeout=5
    )

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhatsApp Style Chat")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ECE5DD")

        self.username = simpledialog.askstring("Username", "Enter username")


# ===== Header =====
        header = tk.Frame(self.root, bg="#075E54", height=60)
        header.pack(fill="x")

        title = tk.Label(
    header,
    text="Real Time Chat App",
    bg="#075E54",
    fg="white",
    font=("Arial", 18, "bold")
)
        title.pack(side="left", padx=20, pady=15)


# ===== Main Container =====
        main_frame = tk.Frame(self.root, bg="#ECE5DD")
        main_frame.pack(fill="both", expand=True)


# ===== Chat Section =====
        chat_frame = tk.Frame(main_frame, bg="#ECE5DD")
        chat_frame.pack(side="left", fill="both", expand=True)


        self.canvas = tk.Canvas(chat_frame, bg="#ECE5DD", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(chat_frame, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#ECE5DD")

        self.scrollable_frame.bind(
    "<Configure>",
    lambda e: self.canvas.configure(
        scrollregion=self.canvas.bbox("all")
    )
)

        self.canvas.create_window(
    (0, 0),
    window=self.scrollable_frame,
    anchor="nw"
)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


# ===== Online Users Sidebar =====
        users_frame = tk.Frame(main_frame, bg="white", width=250)
        users_frame.pack(side="right", fill="y")

        users_label = tk.Label(
        users_frame,
        text="Online Users",
    bg="white",
    fg="black",
    font=("Arial", 16, "bold")
)
        users_label.pack(pady=20)

        self.users_list = tk.Listbox(
        users_frame,
        font=("Arial", 13),
        bg="white",
        bd=0
)
        self.users_list.pack(fill="both", expand=True, padx=15, pady=10)


# Example users
        #self.users_list.insert(tk.END, "🟢 hari")
        self.users_list.insert(tk.END, f"🟢 {self.username}")


# ===== Bottom Input Area =====
        self.bottom_frame = tk.Frame(self.root, bg="#ECE5DD", height=80)
        self.bottom_frame.pack(fill="x", pady=10)

        self.msg_entry = tk.Entry(
    self.bottom_frame,
    font=("Arial", 14),
    bd=0,
    relief="flat"
)
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=15, ipady=12)
        self.msg_entry.bind("<Return>", self.write_message)

        self.send_button = tk.Button(
    self.bottom_frame,
    text="Send",
    command=self.send_message,
    bg="#25D366",
    fg="white",
    font=("Arial", 14, "bold"),
    bd=0,
    padx=25
)
        self.send_button.pack(side="right", padx=15)
        self.file_button = tk.Button(
    self.bottom_frame,
    text="📎",
    bg="#128C7E",
    fg="white",
    command=self.send_file
)

        self.file_button.pack(side=tk.RIGHT, padx=5)
        

        # Emoji Buttons
        emoji_frame = tk.Frame(self.root, bg="#ECE5DD")
        emoji_frame.pack()

        emojis = [
            ("😊", ":smile:"),
            ("❤️", ":heart:"),
            ("🔥", ":fire:"),
            ("👍", ":thumbs:"),
            ("🎉", ":party:")
        ]

        for emoji, code in emojis:
            tk.Button(
                emoji_frame,
                text=emoji,
                command=lambda c=code: self.add_emoji(c)
            ).pack(side=tk.LEFT)

        self.load_chat_history()

        # Socket
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.client.connect((HOST, PORT))

        threading.Thread(
            target=self.receive,
            daemon=True
        ).start()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.stop
        )

        self.root.mainloop()



    def send_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            try:
                filename = os.path.basename(file_path)

                with open(file_path, "rb") as file:
                    file_data = file.read()
                header = f"FILE:{filename}:{len(file_data)}"
                self.client.send(header.encode("utf-8"))
                self.client.sendall(file_data)
                self.display_message(
                           f"📎 Sent: {filename}",
                "me"
            )

            except Exception as e:
                print("File send error:", e)

    def save_message(self, message, sender):
        filename = f"{self.username}_chat.json"

        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
        else:
            data = []

        data.append({
            "sender": sender,
            "message": message
        })

        with open(filename, "w") as file:
            json.dump(data, file)

    def load_chat_history(self):
        filename = f"{self.username}_chat.json"

        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)

                for msg in data:
                    self.display_message(
                        msg["message"],
                        msg["sender"]
                    )

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')

                print("RAW MESSAGE:", repr(message))

                if message == "USERNAME":
                    self.client.send(self.username.encode('utf-8'))

                elif message.startswith("USERS:"):
                    pass

                elif "joined the chat!" in message or "left the chat!" in message:
                    self.display_message(message, "other")

                elif message.startswith("FILE:"):
                    _, sender,filename, filesize = message.split(":")
                    filesize = int(filesize)

                    file_data = b""
                    while len(file_data) < filesize:
                        chunk = self.client.recv(4096)
                        if not chunk:
                            break
                        file_data += chunk
                    if sender!=self.username:
                        with open(f"received_{filename}", "wb") as file:
                            file.write(file_data)

                        self.display_file_message(filename,"other")
                        self.save_message(f"FILE: {filename}", "other")
                        if self.root.state() == "iconic":
                            self.show_notification(sender, f"Sent a file: {filename}")

                elif ": " in message:
                    sender, msg = message.split(": ", 1)

                    if sender != self.username:
                        self.display_message(msg, "other")
                        self.save_message(msg, "other")
                        if self.root.state() == "iconic":
                            self.show_notification(sender, msg)

                else:
                    print("Unknown message:", message)

            except Exception as e:
                print("RECEIVE ERROR:", e)
                break

    def display_message(self, message, sender):
        time = datetime.now().strftime("%I:%M %p")

        outer = tk.Frame(self.scrollable_frame, bg="#ECE5DD")
        outer.pack(fill="x", pady=6, padx=10)

        bubble_color = "#DCF8C6" if sender == "me" else "white"

        bubble = tk.Label(
        outer,
        text=f"{message}\n{time}",
        bg=bubble_color,
        fg="black",
        font=("Arial", 12),
        padx=15,
        pady=10,
        wraplength=350,
        justify="left",
        bd=1,
        relief="solid"
    )

        if sender == "me":
            bubble.pack(anchor="e", padx=20)
        else:
            bubble.pack(anchor="w", padx=20)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def send_message(self):
        message = self.msg_entry.get().strip()

        if message:
            for code, emoji in EMOJIS.items():
                message = message.replace(code, emoji)

            self.display_message(message, "me")
            self.save_message(message, "me")

            try:
                self.client.send(
                f"{self.username}: {message}".encode("utf-8")
            )
            except:
                self.display_message("Connection lost", "other")

            self.msg_entry.delete(0, tk.END)


    def display_file_message(self, filename):
        outer = tk.Frame(self.scrollable_frame, bg="#ECE5DD")
        outer.pack(fill="x", pady=6, padx=10)

        file_btn = tk.Button(
        outer,
        text=f"📎 Open {filename}",
        bg="white",
        fg="blue",
        font=("Arial", 12),
        command=lambda: os.startfile(f"received_{filename}")
    )

        file_btn.pack(anchor="w", padx=20)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def write_message(self, event=None):
        message = self.msg_entry.get().strip()

        if message:
            for code, emoji in EMOJIS.items():
                message = message.replace(code, emoji)

            self.display_message(message, "me")
            self.save_message(message, "me")

            try:
                self.client.send(
                    f"{self.username}: {message}".encode('utf-8')
                )
            except:
                self.display_message(
                    "Connection lost",
                    "other"
                )

            self.msg_entry.delete(0, tk.END)

    def add_emoji(self, emoji_code):
        self.msg_entry.insert(
            tk.INSERT,
            emoji_code + " "
        )

    def stop(self):
        try:
            self.client.close()
        except:
            pass

        self.root.destroy()


ChatClient()