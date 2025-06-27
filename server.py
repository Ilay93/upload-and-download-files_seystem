import socket
import os


def get_file_data_from_client(client_sock: socket.socket):
    file_name = client_sock.recv(1024).decode()
    file_size = int(client_sock.recv(1024).decode())
    
    write_file_from_client(client_sock, os.path.join("files_stored", file_name), file_size)


def write_file_from_client(client_sock: socket.socket, path: str, size: int) -> None:
    with open(path, "wb") as file:
        while size > 0:
            chunk = client_sock.recv(1024)
            file.write(chunk)
            size -= len(chunk)


def send_file_data(client_sock: socket.socket) -> None:
    file_name = client_sock.recv(1024).decode()
    file_full_path = os.path.join("files_stored", file_name)
    if os.path.isfile(file_full_path):
        client_sock.send("1".encode())
        file_size = os.path.getsize(file_full_path)
        data = get_file_data(file_full_path)
        client_sock.send(str(file_size).encode())
        client_sock.sendall(data)
    else:
        client_sock.send("0".encode())


def get_file_data(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        data = file.read()
    return data


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080))

    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        method = client_socket.recv(1024).decode()

        if method == "upload":
            get_file_data_from_client(client_socket)
        elif method == "download":
            send_file_data(client_socket)
        else:
            print(method)

if __name__ == "__main__":
    main()