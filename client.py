import socket
import os



def send_file(sock: socket.socket, file_path: str, file_name: str) -> None:
    
    sock.send(file_name.encode())

    file_size = os.path.getsize(file_path)
    sock.send(str(file_size).encode())

    with open(os.path.join(file_path, file_name), mode="rb") as file:
        data = file.read()
    
    sock.sendall(data)

if __name__ == "__main__":
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 8080))
    file_path = input("enter file path (without the name of the file): ")
    file_name = input("Enter file name: ")
    if not os.path.exists(os.path.join(file_path, file_name)):
        my_socket.close()
        raise Exception(f"The path you specified {os.path.join(file_path, file_name)} does not exist")
    send_file(my_socket, file_path, file_name)
    
    my_socket.close()