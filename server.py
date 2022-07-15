from logging import exception
import socket
import threading
import pickle
import time
import json
import os

from numpy import number
import feature
# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill

import server_functions as sf
# import feature

HOST = "26.165.5.75"
SERVER_PORT = 55544
FORMAT = "utf8"
BUFFER_IMG = 4096

LOGIN = "login"
SIGNUP = "signup"
SEARCH = "search"
BOOKING = "booking"
CANCEL_BOOKING = "cancel booking"
EXIT = "exit"

BUFFER = 10240


def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):

        list.append(item)
        # response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)

    return list


def send_image(conn, file_path):
    image = open(file_path, "rb")
    image_packet = image.read(BUFFER)
    image_size = os.path.getsize(file_path)

    number_of_packets = int(image_size / BUFFER) + 1

    # print(number_of_packets)

    conn.send(str(number_of_packets).encode(FORMAT))
    conn.recv(BUFFER)

    for i in range(number_of_packets):
        conn.send(image_packet)
        image_packet = image.read(BUFFER)
        conn.recv(BUFFER)

    # while image_packet:
    #     conn.send(image_packet)
    #     image_packet = image.read(BUFFER)

    image.close()

    return True


def handleClient(conn: socket, addr, data):

    # Login
    data_hotel = data[0]
    data_hotel_num = data[1]
    data_user = data[2]
    data_bill = data[3]
    data_bill_num = data[4]

    path_file = "Data/Hotel/Image/H0_1D0.jpg"

    print("conn:", conn.getsockname())
    print("addr:", addr)

    msg = None
    index_user = 0
    while True:
        msg = conn.recv(BUFFER)
        msg = pickle.loads(msg)

        print("msg:", msg)

        if (msg[0] == LOGIN):
            # Write your function to log in here
            check = feature.CheckLogin_Sever(data_user, msg)[0]
            conn.sendall(str(check).encode(FORMAT))
            index_user = feature.CheckLogin_Sever(data_user, msg)[1]
        elif (msg[0] == SIGNUP):
            # Write your function to sign up here
            new_user = msg[1]
            data_user.append(new_user.__dict__)
            if(link_data.save_data_user(data_user) == True):
                conn.sendall("Success".encode(FORMAT))
            else:
                conn.sendall("Failed".encode(FORMAT))
        elif (msg[0] == SEARCH):
            # Write your function to search hotel here

            print("received: ")
            print(msg)

            target = {
                "name": msg[1],
                "check_in": msg[2],
                "check_out": msg[3]
            }

            number_of_results, results = sf.search_hotel(target, data_hotel)

            conn.send(str(number_of_results).encode())
            conn.recv(BUFFER)

            for found_result in results:
                stream = pickle.dumps(found_result)
                conn.send(stream)
                conn.recv(BUFFER)

            print("Finished sending")

            confirm_download = conn.recv(BUFFER).decode(FORMAT)

            if confirm_download == "1":
                for each_room in results:
                    for each_image in each_room.image_path:
                        if send_image(conn, "Data/Hotel/Image/" + each_image + ".jpg"):
                            conn.recv(BUFFER)

                print("Images sent")

        elif (msg[0] == BOOKING):
            # Write your function to booking hotel here
            msg.remove(msg[0])
            msg[2] = int(msg[2])
            reply = feature.booking(msg, data_hotel, data_bill, data_user)
            if(reply == "Success: Booking room successfully"):
                conn.sendall(reply.encode(FORMAT))
                send_bill = pickle.dumps(data_bill[len(data_bill)-1])
                conn.sendall(send_bill)
            else:
                conn.sendall(reply.encode(FORMAT))
        elif (msg[0] == CANCEL_BOOKING):
            # Write your function to cancel booking hotel here
            list_bill = feature.Find_Cancel_Bill(
                data_bill, data_user[index_user], data_hotel)
            send_list_bill = pickle.dumps(list_bill)
            conn.sendall(send_list_bill)
            if(len(list_bill) != 0):
                bill_ID_cancel = conn.recv(4096).decode(FORMAT)
                check_cancel = bill.Bill.cancel_bill(
                    data_user[index_user], bill_ID_cancel, data_bill)
                link_data.save_bill_data(
                    "Data\Bill.json", data_bill, len(data_bill))
                link_data.save_data_user(data_user)
                link_data.save_hotel_data(
                    "Data/Hotel/Hotel_Data.json", data_hotel, len(data_hotel))
                conn.sendall(str(check_cancel).encode(FORMAT))
        elif (msg[0] == EXIT):
            # Write your function to exit server here
            break
        else:
            print("Error")
            break

    print("client", addr, "has left the sever")
    print(conn.getsockname(), "closed")
    conn.close()


def main():
    data = link_data.load_full_data()
    link_data.auto_update_room_status(data[0])
    link_data.save_hotel_data(
        "Data/Hotel/Hotel_Data.json", data[0], len(data[0]))

    # You can write the functions for socket here
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, SERVER_PORT))
    s.listen()

    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))

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
            print(nClient)

        except exception:
            print("Error")
            print(exception)

        nClient += 1

    print("End")

    s.close()
    # Here is used to test functions in link_data.py
    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))


if __name__ == "__main__":
    main()
