import socket 
import threading 

#192.168.1.119
HOST = "127.0.0.1" 
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
        if (msg == "list"):
            #response
            conn.sendall(msg.encode(FORMAT))
            list = recvList(conn)

            print("received: ")
            print(list)
    
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

#-----------------------main-------------
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


