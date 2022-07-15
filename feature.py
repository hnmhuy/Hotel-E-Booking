import time
from numpy import number
from PIL import Image
import user
import hotel
import user
import bill

import link_data
from os import system, name


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def ask_to_continue():
    while True:
        print("Do you want to continue? (Y/N)")
        choice = input().upper()
        if(choice == "Y"):
            return True
        elif(choice == "N"):
            return False
        else:
            print("Error: Invalid input")
            continue


def CheckLogin_Sever(data, list):
    i = 0
    while(i < len(data)):
        account_username = data[i]['username']
        account_password = data[i]['password']
        if(list[1] == account_username and list[2] == account_password):
            return [True, i]
        else:
            i += 1
    return [False, -1]


def get_cancel_bill_id(list_available_cancel_bill):
    print(
        "You have " + str(len(list_available_cancel_bill)) + " available to cancel bill")
    for i in range(len(list_available_cancel_bill)):
        print(str(i + 1) + ". " + list_available_cancel_bill[i].bill_id)
    while True:
        choice = input(
            "Select index for view more detail (type 0 to return): ")
        if(choice == "0"):
            break
        elif(choice.isnumeric() and int(choice) <= len(list_available_cancel_bill)):
            bill.print_bill(
                list_available_cancel_bill[int(choice) - 1])
            print("=========================")
            print("Do you want to cancel this bill? (Y/N)")
            is_cancel = input().upper()
            if(is_cancel == "Y"):
                return list_available_cancel_bill[int(choice) - 1].bill_id
            elif(is_cancel == "N"):
                continue
            else:
                print("Error: Invalid input")
                continue
    return None


def Find_Cancel_Bill(data_bill, data_user, data_hotel):
    list_available_to_cancel_bill = []
    list_bill_id = data_user["bill"]
    if not (list_bill_id):
        return list_available_to_cancel_bill
    for bill_id in list_bill_id:
        decode = bill_id.split("_")
        index_bill = int(decode[1])
        hotel_id = decode[0][1:len(decode[0])]
        current_bill = data_bill[index_bill-1]
        if(bill.Bill.available_to_cancel(current_bill) == True and current_bill.cancel == False):
            bill.Bill.load_room_data_from_data_base(
                current_bill, hotel.find_hotel_by_id(data_hotel, hotel_id))
            list_available_to_cancel_bill.append(current_bill)

    return list_available_to_cancel_bill


# Constant for all server functions
LOGIN = "login"
SIGNUP = "signup"
SEARCHING = "searching"
BOOKING = "booking"
CANCEL_BOOKING = "cancel booking"
EXIT = "exit"


room_type_single = 'Single'
room_type_double = 'Double'
room_type_family = 'Family'

date_format = "%d/%m/%Y"

hotel_path = "Data/Hotel/Hotel_Data.json"
bill_path = "Data/Bill.json"

'''To book a room, the user must login first.
   Then the server receives the information including:
    - Hotel id/ hotel name
    - Number of room
    - Type of room
    - Date check in
    - Date check out
    - Note

    Then, find out the the data of hotel and check the availability of room.
    If all the room is availiable, then create a bill and update the room status.
    Else, return error message.'''

# THESE FUNCTION IS USE TO BOOK ROOMS

'''Info_booking is decode following format:
    - info_booking[0] = user_name
    - info_booking[1] = hotel_id / hotel_name
    - info_booking[2] = number of room
    - info_booking[3] = type of room
    - info_booking[4] = date check in
    - info_booking[5] = date check out
    - info_booking[6] = note'''


def booking(info_booking, data_hotel, data_bill, data_user):

    # Get the hotel id
    if (hotel.is_hotel_id(info_booking[1])):
        hotel_id = info_booking[1]
    else:
        hotel_id = hotel.ret_hotel_id(info_booking[1], data_hotel)

    # Get the number of room
    number_of_room = int(info_booking[2])

    # Get the type of room
    if(info_booking[3].upper() == "SINGLE"):
        room_type = room_type_single
    elif(info_booking[3].upper() == "DOUBLE"):
        room_type = room_type_double
    elif(info_booking[3].upper() == "FAMILY"):
        room_type = room_type_family
    else:
        return "Error: Invalid room type"

    # Get the date check in and check out
    date_check_in = time.strptime(info_booking[4], date_format)
    date_check_out = time.strptime(info_booking[5], date_format)

    # Get the note
    note = info_booking[6]

    # Find and get data hotel
    chosen_hotel = hotel.find_hotel_by_id(data_hotel, hotel_id)
    if (chosen_hotel is None):
        return "Error: Hotel not found"

    # Check the availability of room
    count_available_room = 0
    list_of_room_id = []
    list_room = []

    for room in chosen_hotel.list_room:
        if(room.room_type == room_type):
            available_to_book = True
            check_in = time.mktime(date_check_in)
            check_out = time.mktime(date_check_out)
            if(room.user_book == None):
                available_to_book = True
            else:
                for i in range(len(room.user_book)):
                    # Check date check in and date check out is available
                    curr_check_in = time.mktime(room.date_check_in[i])
                    curr_check_out = time.mktime(room.date_check_out[i])
                    if(check_in >= curr_check_in and check_in <= curr_check_out):
                        available_to_book = False
                        break
                    elif (check_out >= curr_check_in and check_out <= curr_check_out):
                        available_to_book = False
                        break
                    elif check_in <= curr_check_in and check_out >= curr_check_out:
                        available_to_book = False
                        break
            if(available_to_book):
                count_available_room += 1
                list_of_room_id.append(room.room_id)
                list_room.append(room)
        if(count_available_room == number_of_room):
            break

    if(count_available_room < number_of_room):
        return "Error: Not enough room"
    else:
        for each_room in list_room:
            if each_room.user_book == None:
                each_room.user_book = []
                each_room.date_check_in = []
                each_room.date_check_out = []
            each_room.user_book.append(info_booking[0])
            each_room.date_check_in.append(date_check_in)
            each_room.date_check_out.append(date_check_out)

    # Create a bill
    print(bill.Bill.create_bill(chosen_hotel,
                                list_of_room_id, info_booking[0], data_bill)[0])

    # Update json file
    link_data.update_bill_in_user(
        info_booking[0], data_bill[len(data_bill) - 1].bill_id, data_user)
    link_data.save_hotel_data(hotel_path, data_hotel, len(data_hotel))
    link_data.save_bill_data(bill_path, data_bill, len(data_bill))
    return "Success: Booking room successfully"


def display_search_results(keywords, result_list):
    print("Hotel name: " + keywords[0])
    print("Check in date: " + keywords[1])
    print("Check out date: " + keywords[2])

    print("\nAvailable room list:")
    for room in result_list:
        print("=========================")
        print("Room id:   ", room.room_id)
        print("Room type:  ", room.room_type)
        print("Room price: ", room.room_price)
        print("Descriton: \n", room.description)
        print("=========================")
    return "Success: Booking room successfully"


def display_image(file_list):
    print("Downloaded images:")

    for i in range(len(file_list)):
        print(str(i + 1) + ". " + file_list[i])

    choice = input("Select index for showing (type 0 to return): ")

    while (not choice.isnumeric() or
            (choice.isnumeric() and int(choice) > len(file_list))):
        choice = input("Invalid input, please retry: ")

    while int(choice) != 0:
        while (not choice.isnumeric() or
                (choice.isnumeric() and int(choice) > len(file_list))):
            choice = input("Invalid input, please retry: ")

        img = Image.open("Client_Downloads/" +
                         file_list[int(choice) - 1] + ".jpg")
        img.show()

        choice = input("Select index for showing (type 0 to return): ")
        while not choice.isnumeric():
            choice = input("Invalid input, please retry: ")


def get_info_booking(user_name):
    msg = []
    msg.append(BOOKING)
    msg.append(user_name)
    hotel = input("Enter the name or id of hotel: ")
    msg.append(hotel)
    while True:
        try:
            number_of_room = None
            number_of_room = int(input("Enter the number of room: "))
            msg.append(str(number_of_room))
            break
        except ValueError:
            print("Error: Invalid number of room")
    while True:
        room_type = str(input("Enter the type of room: "))
        room_type = room_type.upper()
        if(room_type != "SINGLE" and room_type != "DOUBLE" and room_type != "FAMILY"):
            print("Error: Invalid room type")
        else:
            break
    msg.append(room_type)
    while True:
        try:
            date_check_in = None
            date_check_in = input("Enter the date check in: ")
            time.strptime(date_check_in, date_format)
            # Check the date check in is greater than today
            if(time.strptime(date_check_in, date_format) < time.strptime(time.strftime(date_format, time.localtime()), date_format)):
                print("Error: You must to choose a date greater than today")
            else:
                break
        except ValueError:
            print("Error: Invalid date check in")
    msg.append(date_check_in)
    while True:
        try:
            date_check_out = None
            date_check_out = input("Enter the date check out: ")
            time.strptime(date_check_out, date_format)
            # Check the date check out is greater than check in
            if(time.strptime(date_check_out, date_format) < time.strptime(date_check_in, date_format)):
                print("Error: You must to choose a date greater than check in")
            else:
                break
        except ValueError:
            print("Error: Invalid date check out")
    msg.append(date_check_out)
    note = input("Enter the note: ")
    msg.append(note)
    return msg
