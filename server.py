import socket
import threading
import pickle
import time

# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill

import server_functions as sf 
# import feature

HOST = "127.0.0.1"
SERVER_PORT = 65500
FORMAT = "utf8"
BUFFER_IMG = 4096

LOGIN = "login"
SIGNUP = "signup"
SEARCH = "search"
BOOKING = "booking"
CANCEL_BOOKING = "cancel booking"
EXIT = "exit"

# # Load hotel data from file
# root_path = "Data/"
# file_path = root_path + "/Hotel/Hotel_Data.json"
# hotel_data = link_data.convert_json_to_class_hotel(
#                     link_data.read_hotel_data(file_path))
        
def CheckLogin(conn):
    account_list = recvList(conn)
     
def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

def handleClient(conn: socket, addr, data):

    # Login
    data_hotel = data[0]
    data_hotel_num = data[1]
    data_user = data[2]
    data_bill = data[3]
    data_bill_num = data[4]

    path_file = "Data/Hotel/Image/H0_1D0.jpg"

    print("conn:", conn.getsockname())

    # Send welcome message
    # conn.sendall("Welcome to the server".encode(FORMAT))
    msg = None

    while True:
        msg = conn.recv(1024)
        msg = pickle.loads(msg)

        # msg = recvList(conn)

        print("msg:", msg)
        if (msg[0] == LOGIN):
            # Write your function to log in here
            break
        elif (msg[0] == SIGNUP):
            # Write your function to sign up here
            break
        elif (msg[0] == SEARCH):
            # Write your function to search hotel here

            # conn.sendall(msg.encode(FORMAT))
            # search_info = recvList(conn)

            print("received: ")
            print(msg)

            target = {
                "name": msg[1],
                "check_in": msg[2],
                "check_out": msg[3]
            }

            number_of_results, results = sf.search_hotel(target, data_hotel)

            conn.send(str(number_of_results).encode())
            conn.recv(1024)

            for found_result in results:
                stream = pickle.dumps(found_result)
                conn.send(stream)
                conn.recv(1024)

            print("Finished sending")

            print(conn.recv(1024).decode(FORMAT))

        elif (msg[0] == BOOKING):
            # Write your function to booking hotel here
            break
        elif (msg[0] == CANCEL_BOOKING):
            # Write your function to cancel booking hotel here
            break
        elif (msg[0] == "exit"):
            break
        else:
            print("Error")
            break
    
    # print("conn:",conn.getsockname())
    # msg = None
    # while (msg != "x"):
    #     msg = conn.recv(1024).decode(FORMAT)
    #     print("client ",addr, "says", msg)
        
    #     if(msg == LOGIN):
    #         conn.sendall(msg.encode(FORMAT))
    #         list = recvList(conn)
    #         print("received: ")
    #         print(list)
        
    #     # Search function
    #     if(msg == SEARCH):
    #         conn.sendall(msg.encode(FORMAT))
    #         search_info = recvList(conn)
    #         print("received: ")
    #         print(search_info)

    #         target = {
    #             "name": search_info[0],
    #             "check_in": search_info[1],
    #             "check_out": search_info[2]
    #         }

    #         results = sf.search_hotel(target, hotel_data)

    #         # print(type(results))

    print("client" , addr, "has left the sever")
    print(conn.getsockname(), "closed")
    conn.close()
              
clients = {}
addresses= {}
HOST= "127.0.0.1"
SERVER_PORT = 65432
BUFSIZE = 1024
FORMAT = "utf8"

def main():

    data = link_data.load_full_data()

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
    while (nClient < 3):
        try:
            conn, addr = s.accept()
            thr = threading.Thread(target=handleClient, args=(conn,addr,data))
            thr.daemon = False
            thr.start()

        except:
            print("Error")
        
        nClient += 1
    print("End")
    input()
    s.close();
    # Here is used to test functions in link_data.py
    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))
    
    # test push main


if __name__ == "__main__":
    main()
