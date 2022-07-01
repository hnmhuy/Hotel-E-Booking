import socket
import user

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

LOGIN = "login"
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


except:
    print("Error")


client.close()