import socket
import os


def send_file(sock: socket.socket, file_path: str, file_name: str) -> None:
    sock.send("upload".encode())
    sock.send(file_name.encode())

    file_size = os.path.getsize(file_path)
    sock.send(str(file_size).encode())

    with open(os.path.join(file_path, file_name), mode="rb") as file:
        data = file.read()

    sock.sendall(data)


def download_file_from_server(sock: socket.socket, download_file_name: str, save_file_path: str) -> None:
    sock.send("download".encode())
    sock.send(download_file_name.encode())
    
    status = sock.recv(1024).decode()
    if status == "1":
        size = int(sock.recv(1024).decode())
        data_remaining = size
        with open(os.path.join(save_file_path, download_file_name), "wb") as file:
            while data_remaining > 0:
                chunk = sock.recv(1024)
                file.write(chunk)
                data_remaining -= len(chunk)
    else:
        print("The file you wrote does not exist")
    


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 8080))
 
    upload_or_download_option = input("Enter action download/upload: ")
    while upload_or_download_option != "download" and upload_or_download_option != "upload":
        upload_or_download_option = input("You didn't enter one of the options. Enter action download/upload: ")

    if upload_or_download_option == "upload":
        file_path = input("enter the path for the file you want to upload (without the name of the file): ")
        file_name = input("Enter the name of the file you want to download: ")

        while not os.path.exists(os.path.join(file_path, file_name)):
            print(f"The file location: {os.path.join(file_path, file_name)} you entered does no exist ")
            file_path = input("enter file path (without the name of the file): ")
            file_name = input("Enter file name: ")

        send_file(my_socket, file_path, file_name)
    
    else:
        file_to_download = input("Enter the name of the file you want to download: ").strip()
        while file_to_download == "":
            file_to_download = input("You didn't write a file name, Enter the name of the file you want to download: ")
        folder_path_to_save = input("Enter the location of the folder you want to save the file in: ")
        
        if os.path.isdir(folder_path_to_save):
            download_file_from_server(my_socket, file_to_download, folder_path_to_save)
        else:
            print("You didn't specify a proper folder location")
    
    my_socket.close()


if __name__ == "__main__":
    main()