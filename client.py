import socket
from urllib import response

from numpy import number
import user
import pickle

import feature as cf

# HOST = "127.0.0.1"
HOST = "26.165.5.75"
SERVER_PORT = 55544
import feature
import bill

FORMAT = "utf8"

LOGIN = "login"
SEARCH = "search"
BOOKING = "booking"
SIGNUP = "signup"
CANCEL_BOOKING = "cancel booking"
EXIT = "exit"

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


def search_interface():
    search_info = []

    hotel_name = input("Type in hotel name: ")
    search_info.append(hotel_name)

    check_in_date = input("Check in date (DD/MM/YYYY): ")
    search_info.append(check_in_date)

    check_out_date = input("Check out date (DD/MM/YYYY): ")
    search_info.append(check_out_date)


    return search_info



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    feature.clear_screen()
    client.connect((HOST, SERVER_PORT))
    print("client address:", client.getsockname())
    msg = None
    print("Connected to server")
    is_login = True
    request = []
    while True:
        request = []    
        print("1. Login")
        print("2. Sign up")
        print("\n")
        choice = input("Please choose: ")
        if choice == "1":
            request.append(LOGIN)
            user_name = input("Username: ")
            user_password = input("Password: ")
            request.append(user_name)
            request.append(user_password)
            request.append("end")

            # sendList(client, request)

            send_data = pickle.dumps(request)
            client.send(send_data)

            is_login = client.recv(1024).decode(FORMAT)
            print(is_login)
            if is_login == "True":
                print("Login success")
                break
            else:
                print("Login failed")
                continue
        elif choice == "2":
            request.append(SIGNUP)
            new_user = user.User.create_new_user()
            request.append(new_user)

            # fullname = new_user.fullname
            # birthday = new_user.birthday
            # username = new_user.username
            # password = new_user.password
            # credit_card = new_user.credit_card
            # cvv = new_user.cvv
            # expiration_date = new_user.expiration_date
            # request.append(fullname)
            # request.append(birthday)
            # request.append(username)
            # request.append(password)
            # request.append(credit_card)
            # request.append(cvv)
            # request.append(expiration_date)

            # sendList(client, request)
            
            send_data = pickle.dumps(request)
            client.send(send_data)

            is_regis = client.recv(1024).decode(FORMAT)
            if(is_regis == "Success"):
                print("Register success")
                continue
            else:
                print("Register failed")
                continue
        break

    while is_login == "True":
        print("1. Searching")
        print("2. Booking")
        print("3. Cancel booking")
        print("4. Logout and exit")
        print("\n")
        
        choice = input("Please choose: ")

        request = []

        if choice == "1":
            # Write your function to search hotel here
            request.append(SEARCH)
            # client.recv(1024)

            info = search_interface()

            for data in info:
                request.append(data)

            # sendList(client, request)
            send_data = pickle.dumps(request)
            client.send(send_data)

            data = client.recv(1024)
            ack = "a"
            client.send(ack.encode())

            number_of_results = int(data.decode())
            search_result = []

            for i in range(number_of_results):
                data = client.recv(1024)
                client.send(ack.encode())
                hotel_room = pickle.loads(data)
                search_result.append(hotel_room)
            
            feature.display_search_results(info, search_result)

        elif choice == "2":
            # Write your function to booking hotel here
            msg = feature.get_info_booking(user_name)
            sendList(client, msg)
            print("Sent booking info to server")
            print("Waiting for server response . . .")
            response = client.recv(1024).decode(FORMAT)
            if response == "Success: Booking room successfully":
                print(response)
                revc_data = client.recv(4096)
                your_bill = pickle.loads(revc_data)
                print("Here is your bill:")
                bill.print_bill(your_bill)
            else:
                print(response)
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


except Exception as e:
    print("Error")
    print(e)


client.close()
