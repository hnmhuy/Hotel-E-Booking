import socket
import threading
import time
# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill

HOST= "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

def handleClient(conn: socket, addr):
    
    print("conn:",conn.getsockname())
    
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)
        
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

def main():

    # You can wirte the functions for socket here
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    s.bind((HOST, SERVER_PORT))
    s.listen()

    print("SERVER SIDE")
    print("server:", HOST, SERVER_PORT)
    print("Waiting for Client")

    nClient = 0
    while (nClient < 3):
        try:
            conn, addr = s.accept()
            
            thr = threading.Thread(target=handleClient, args=(conn,addr))
            thr.daemon = False
            thr.start()

        except:
            print("Error")
        
        nClient += 1

    print("End")

    s.close();
    conn.close()
    # Here is used to test functions in link_data.py
    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))

    # Test printing hotel data
    link_data.print_all_hotel(hotel_data)


if __name__ == "__main__":
    main()
