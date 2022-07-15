from numpy import number
import bill
import socket
import user
import pickle
import time
import math
import feature

HOST = "26.165.5.75"
# HOST = "26.165.5.75"
SERVER_PORT = 55544

FORMAT = "utf8"

LOGIN = "login"
SEARCH = "search"
BOOKING = "booking"
SIGNUP = "signup"
CANCEL_BOOKING = "cancel booking"
EXIT = "exit"

BUFFER = 10240
BUFFER_IMG = 4096


def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        # wait response
        client.recv(1024)

    msg = "end"
    client.send(msg.encode(FORMAT))


def Login(client):
    account = []
    print("Please input username and password")
    username = input('Username:')
    password = input('Password:')
    bool = user.User.check_username_availability(
        username) and user.User.check_password(password)
    while (bool == False):
        print('Please try again')
        print('The maximum length of username is 32 letters ')
        print('The min of pass is 4 and must have lowercase, uppercase, number, special character')
        username = input('Username:')
        password = input('Password:')
        bool = user.User.check_username_availability(
            username) and user.User.check_password(password)
    account.append(username)
    account.append(password)
    sendList(client, account)


def check_date_format(date_string):
    try:
        input_time = time.strptime(date_string, "%d/%m/%Y")
        return True
    except:
        return False


def search_interface():
    search_info = []

    hotel_name = input("Type in hotel name: ")
    search_info.append(hotel_name)

    check_in_date = input("Check in date (DD/MM/YYYY): ")
    while not check_date_format(check_in_date):
        check_in_date = input("Invalid format (DD/MM/YYYY): ")

    search_info.append(check_in_date)

    check_out_date = input("Check out date (DD/MM/YYYY): ")
    while not check_date_format(check_out_date):
        check_out_date = input("Invalid format (DD/MM/YYYY): ")

    search_info.append(check_out_date)

    return search_info


def receive_image(client, file_path):
    data = client.recv(BUFFER)
    number_of_packets = float(data.decode(FORMAT))

    # print(number_of_packets)
    client.send("Size received!".encode(FORMAT))

    image = open(file_path, "wb")

    for packet in range(math.ceil(number_of_packets)):
        # print(file_path)
        image_packet = client.recv(BUFFER)
        image.write(image_packet)

    image.close()

    return True


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

    # Image sending test

    while True:
        time.sleep(1.5)
        feature.clear_screen()
        print("WELCOME TO HOTEL BOOKING SYSTEM")
        print("=================================")
        print()

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
            send_data = pickle.dumps(request)
            client.send(send_data)

            is_regis = client.recv(1024).decode(FORMAT)
            if(is_regis == "Success"):
                print("Register success")
                continue
            else:
                print("Register failed")
                continue
        else:
            print("Invalid input")
            continue
        break

    flag = True
    time.sleep(1)
    while is_login == "True":

        feature.clear_screen()
        print("BOOKING HOTEL SYSTEM")
        print("====================")
        print()
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

            data = client.recv(BUFFER)
            ack = "a"
            client.send(ack.encode())

            number_of_results = int(data.decode())
            search_result = []

            for i in range(number_of_results):
                data = client.recv(BUFFER)
                hotel_room = pickle.loads(data)
                search_result.append(hotel_room)
                client.send(ack.encode())

            feature.display_search_results(info, search_result)

            print("Do you want to download the room images?")
            print("1. Yes")
            print("2. No\n")

            confirm_send = input("Your choice: ")

            while (confirm_send != "1" and confirm_send != "2"):
                confirm_send = input("Invalid input, please re-enter: ")

            client.send(confirm_send.encode(FORMAT))

            if confirm_send == "1":
                downloaded_images = []

                for each_room in search_result:
                    for each_image in each_room.image_path:
                        if receive_image(client, "Client_Downloads/" + each_image + ".jpg"):
                            client.send("RECEIVED".encode())

                            if each_image not in downloaded_images:
                                downloaded_images.append(each_image)

                print("Photos are downloaded in Client_Downloads\n")
                print("Do you want to see the room images?")
                print("1. Yes")
                print("2. No\n")

                confirm_open = input("Your choice: ")
                while (confirm_open != "1" and confirm_open != "2"):
                    confirm_open = input("Invalid input, please re-enter: ")

                if confirm_open == "1":
                    # Let user choose the image
                    feature.display_image(downloaded_images)

            # Press any key to continue
            input("Press any key to continue")

        elif choice == "2":
            # Write your function to booking hotel here
            msg = feature.get_info_booking(user_name)
            client.sendall(pickle.dumps(msg))
            print("Sent booking info to server")
            print("Waiting for server response . . .")
            response = client.recv(4096).decode(FORMAT)
            if response == "Success: Booking room successfully":
                print(response)
                revc_data = client.recv(4096)
                your_bill = pickle.loads(revc_data)
                print("Here is your bill:")
                bill.print_bill(your_bill)
            else:
                print(response)
            # Press any key to continue
            input("Press any key to continue")
        elif choice == "3":
            request.append(CANCEL_BOOKING)
            # Write your function to cancel booking here
            request.append(user_name)
            send_data = pickle.dumps(request)
            client.send(send_data)
            print("\n")
            print("Sent username info to server")
            print("Waiting for server response . . .")
            print("\n")
            data = client.recv(BUFFER)
            list_bill = pickle.loads(data)
            if(len(list_bill) == 0):
                print("No available booking to cancel")
            else:
                bill_id_cancel = feature.get_cancel_bill_id(list_bill)
                if(bill_id_cancel == None):
                    bill_id_cancel = "-1"
                client.sendall(bill_id_cancel.encode(FORMAT))
                print("Waiting for server response . . .")
                is_cancel = client.recv(4096).decode(FORMAT)
                if(is_cancel == "True"):
                    print("\nYOUR CANCEL BOOKING IS SUCCESSFUL\n")
                else:
                    print("\nYOUR CANCEL BOOKING IS UNSUCCESSFUL\n")
            # Press any key to continue
            input("Press any key to continue")
        elif choice == "4":
            request.append(EXIT)
            client.sendall(pickle.dumps(request))
            break

            # Write your function to logout here
        else:
            print("Please choose again")
            continue

except Exception as e:
    print("Error")
    print(e)


client.close()

# input("A")
