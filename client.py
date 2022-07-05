import socket
import user

import client_functions as cf

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

LOGIN = "login"
SEARCH = "search"

def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        #wait response
        client.recv(1024)

    msg = "end"
    client.send(msg.encode(FORMAT))   

def Login(client):
    account = []
    print("Please input username and password")
    username = input('Username:')
    password = input('Password:')
    bool = user.User.check_username_availability(username) and user.User.check_password(password)
    while (bool == False):
       print('Please try again')
       print('The maximum length of username is 32 letters ')
       print('The min of pass is 4 and must have lowercase, uppercase, number, special character')
       username = input('Username:')
       password = input('Password:')
       bool = user.User.check_username_availability(username) and user.User.check_password(password)
    account.append(username)
    account.append(password)
    sendList(client, account)   


def search_interface(client):
    search_info = []

    hotel_name = input("Type in hotel name: ")
    check_in_date = input("Check in date (DD/MM/YYYY): ")
    check_out_date = input("Check out date (DD/MM/YYYY): ")

    search_info.append(hotel_name)
    search_info.append(check_in_date)
    search_info.append(check_out_date)

    sendList(client, search_info)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")


try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())

    msg = None
    while (msg != "x"):
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))
        if (msg == LOGIN):
            # wait response
            client.recv(1024)
            Login(client)

        if (msg == SEARCH):
            client.recv(1024)
            search_interface(client)


except:
    print("Error")


client.close()