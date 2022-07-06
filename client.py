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
    client.connect((HOST, SERVER_PORT))
    print("Connected to server")
    is_login = False
    request = []
    while True:
        # print("1. Login")
        # print("2. Sign up")
        # print("\n")
        # choice = input("Please choose: ")
        # if choice == "1":
        #     request.append(LOGIN)
        #     user_name = input("Username: ")
        #     user_password = input("Password: ")
        #     request.append(user_name)
        #     request.append(user_password)
        #     sendList(client, request)
        #     is_login = client.recv(1024).decode(FORMAT)
        #     if is_login == "True":
        #         print("Login success")
        #         break
        #     else:
        #         print("Login failed")
        #         continue
        # elif choice == "2":
        #     request.append(SIGNUP)
        #     user_name = input("Username: ")
        #     user_password = input("Password: ")
        #     request.append(user_name)
        #     request.append(user_password)
        #     sendList(client, request)
        #     is_login = client.recv(1024).decode(FORMAT)
        #     if is_login == "True":
        #         print("Sign up success")
        #         break
        #     else:
        #         print("Sign up failed")
        #         continue
        break
    while is_login == "True":
        print("1. Searching")
        print("2. Booking")
        print("3. Cancel booking")
        print("4. Logout and exit")
        print("\n")
        choice = input("Please choose: ")
        if choice == "1":
            request.append(SEARCH)
            client.recv(1024)
            search_interface(client)
            # Write your function to search hotel here
        elif choice == "2":
            request.append(BOOKING)
            # Write your function to booking hotel here

        elif choice == "3":
            request.append(CANCEL_BOOKING)
            # Write your function to cancel booking here
        elif choice == "4":
            request.append(EXIT)
            # Write your function to logout here
        else:
            print("Please choose again")
            continue
    # print("client address:", client.getsockname())
    # print("client:", HOST, SERVER_PORT)
    # print("Connected to server")
    # reply = client.recv(1024).decode(FORMAT)
    # print("reply:", reply)
    # msg = None
    # while (msg != "x"):
    #     user_info = ["benn", "122345", "end"]
    #     sendList(client, user_info)
    #     print("user_info:", user_info)
    #     print("Received:", client.recv(1024).decode(FORMAT))
        # msg = input("talk: ")
        # client.sendall(msg.encode(FORMAT))
        # if (msg == "list"):
        #     # wait response
        #     client.recv(1024)
        #     sendList(client, list)
        # elif (msg == "img"):
        #     # Receive the number of packet
        #     num_packet = int(client.recv(1024).decode(FORMAT))
        #     print("num_packet:", num_packet)
        #     with open("test.jpg", "wb") as f:
        #         for i in range(num_packet):
        #             data = client.recv(BUFFER_IMG)
        #             f.write(data)
        #     f.close()
        # Ask to see the image
        # print("Do you want to see the image? (y/n)")
        # answer = input()
        # if (answer == "y"):
        #     img = Image.open("test.jpg")
        #     img.show()
        # else:
        #     print("Image is not shown")
        # msg = input("talk: ")
        # client.sendall(msg.encode(FORMAT))
        # if (msg == LOGIN):
        #     # wait response
        #     client.recv(1024)
        #     Login(client)


except:
    print("Error")


client.close()