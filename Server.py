#Import required modules
import socket
import threading
from decrypto import RSACipher  
import hashlib
import base64


cipher = RSACipher()

HOST = '127.0.0.1'
PORT = 8844  # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users


# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while 1:

        encrypted = client.recv(2048).decode('utf-8')
        if encrypted != '':
            final_msg = username + '~' + encrypted
            final_msg1= final_msg.upper()
            send_messages_to_all(final_msg1)
            keys = cipher.generate_keys(23, 31)
            decrypted = cipher.encrypt(encrypted, keys['public_key'])
            print(decrypted)
            # print(encrypted)

        else:
            print(f"The message send from client {username} is empty")


# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(encryted):
    for user in active_clients:
        send_message_to_client(user[1],encryted )


# Function to handle client
def client_handler(client):
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()


# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(5)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()

        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == '__main__':
    main()