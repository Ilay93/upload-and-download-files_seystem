import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 800))

server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()


    file_name = client_socket.recv(1024).decode()
    file_size = int(client_socket.recv(1024).decode())
    data_left = file_size

    with open(os.path.join("files_stored", file_name), "wb") as file:
        while data_left > 0:
            chunk = client_socket.recv(1024)
            file.write(chunk)
            data_left -= 1024
        
    client_socket.close()