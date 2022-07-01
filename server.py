import pickle
import socket
from this import s
import threading
import time
# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill
import os
from PIL import Image

HOST = "127.0.0.1"
SERVER_PORT = 65500
FORMAT = "utf8"
BUFFER_IMG = 4096


def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):

        list.append(item)
        # response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)

    return list


def handleClient(conn: socket, addr, data):

    # Login
    user_data = data[2]

    path_file = "Data/Hotel/Image/H0_1D0.jpg"
    print("conn:", conn.getsockname())
    # Send welcome message
    conn.sendall("Welcome to the server".encode(FORMAT))
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("msg:", msg)
        user_info = recvList(conn)
        print("user_info:", user_info)
        if (msg == "login"):
            # Check the user information
            if (user_info[0] in user_data):
                if (user_data[user_info[0]].password == user_info[1]):
                    conn.sendall("login success".encode(FORMAT))
                    # Send the user information
                    conn.sendall(pickle.dumps(user_data[user_info[0]]))
                else:
                    conn.sendall("login failed".encode(FORMAT))
            else:
                conn.sendall("login failed".encode(FORMAT))
        # if(msg == "img"):
        #     # Get image size
        #     size_img = os.path.getsize(path_file)
        #     num_packet = int(size_img / BUFFER_IMG) + 1
        #     conn.send(str(num_packet).encode(FORMAT))
        #     with open(path_file, "rb") as f:
        #         for i in range(num_packet):
        #             data = f.read(BUFFER_IMG)
        #             conn.sendall(data)
        #     f.close()
        # Send image

    print("client", addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()


def main():
    data = link_data.load_full_data()
    # You can wirte the functions for socket here
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, SERVER_PORT))
    s.listen()

    print("SERVER SIDE")
    print("server:", HOST, SERVER_PORT)
    print("Waiting for Client")

    nClient = 0
    while (nClient < 10):
        try:
            conn, addr = s.accept()

            thr = threading.Thread(target=handleClient,
                                   args=(conn, addr, data))
            thr.daemon = False
            thr.start()

        except:
            print("Error")

        nClient += 1

    print("End")

    s.close()
    conn.close()
    # Here is used to test functions in link_data.py
    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))

    # test push main


if __name__ == "__main__":
    main()
