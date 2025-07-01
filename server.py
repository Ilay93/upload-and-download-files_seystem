import socket
import os


def get_file_data_from_client(client_sock: socket.socket):
    file_name = client_sock.recv(1024).decode()
    file_size = int(client_sock.recv(30).decode())
    data_remaining = file_size
    with open(os.path.join("files_stored", file_name), "wb") as file:
        while data_remaining > 0:
            chunk = client_sock.recv(1024)
            file.write(chunk)
            data_remaining -= len(chunk)


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
        method = client_socket.recv(1).decode()

        if method == "0":
            get_file_data_from_client(client_socket)
        elif method == "1":
            send_file_data(client_socket)
        else:
            print(method)

if __name__ == "__main__":
    main()