import socket
import threading
import time
import json
# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill
LOGIN = "login"
SIGNUP = "signup"
def CheckLogin(conn, data, list):
    i=0
    while(i < len(data['users'])):
        account_username = data['users'][i]['username']
        account_password = data['users'][i]['password']
        if(list[0] == account_username and list[1] == account_password ):
            check = True
            break
        else:
            check = False
            i+=1
    if(check == True):
       print("Login Successfully")
    else:
       print("Failed to login")
            
     
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
    
    print("conn:",conn.getsockname())
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)
        
        if(msg == LOGIN):
            conn.sendall(msg.encode(FORMAT))
            list = recvList(conn)
            print("received: ")
            print(list)
            #CheckLogin(conn,data,list)
        if(msg ==SIGNUP):
            conn.sendall(msg.encode(FORMAT))
            User = recvList(conn)
            print("received: ")
            print(User)
            

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

    # You can write the functions for socket here
    with open("Data\\User.json","r") as fin:
        data = json.load(fin)
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
