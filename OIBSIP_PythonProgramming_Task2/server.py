import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")

clients = []
usernames = []


# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Send updated user list
def update_user_list():
    user_data = "USERS:" + ",".join(usernames)
    broadcast(user_data.encode('utf-8'))


# Handle messages
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)

            clients.remove(client)
            client.close()

            username = usernames[index]
            usernames.remove(username)

            broadcast(f"{username} left the chat!".encode('utf-8'))

            update_user_list()

            print(f"{username} disconnected")
            break


# Receive connections
# Receive connections
def receive():
    while True:
        client, address = server.accept()

        print(f"Connected with {str(address)}")

        client.send("USERNAME".encode('utf-8'))

        username = client.recv(1024).decode('utf-8')

        usernames.append(username)
        clients.append(client)

        print(f"Username: {username}")

        broadcast(f"{username} joined the chat!".encode('utf-8'))

        update_user_list()

        client.send("Connected to server!".encode('utf-8'))

        # FIXED LINE
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()