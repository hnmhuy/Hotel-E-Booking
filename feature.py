import time
from numpy import number
import user
import hotel
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


def CheckLogin_Sever(data, list):
    i = 0
    while(i < len(data)):
        account_username = data[i]['username']
        account_password = data[i]['password']
        if(list[1] == account_username and list[2] == account_password):
            return True
        else:
            i += 1
    return False


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


def booking(info_booking, data_hotel, data_bill):

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

    if(number_of_room > chosen_hotel.number_available_room):
        return "Error: Not enough room"

    # Check the availability of room
    count_available_room = 0
    list_of_room_id = []
    list_room = []
    for room in chosen_hotel.list_room:
        if(room.room_type == room_type and room.room_availability == True):
            count_available_room += 1

    if(count_available_room < number_of_room - 1):
        return "Error: Not enough room"
    else:
        # Create a bill
        for room in chosen_hotel.list_room:
            if(room.room_type == room_type and room.room_availability == True):
                count_available_room += 1
                # Update the room status
                room.room_availability = False
                room.user_book = info_booking[0]
                room.date_check_in = date_check_in
                room.date_check_out = date_check_out
                list_of_room_id.append(room.room_id)
                list_room.append(room)
            if(count_available_room == number_of_room - 1):
                break

        # Create a bill
        print(bill.Bill.create_bill(chosen_hotel,
              list_of_room_id, info_booking[0], data_bill)[0])

    # Update json file
    link_data.save_hotel_data(hotel_path, data_hotel, len(data_hotel))
    link_data.save_bill_data(bill_path, data_bill, len(data_bill))
    return "Success: Booking room successfully"


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
            break
        except ValueError:
            print("Error: Invalid date check out")
    msg.append(date_check_out)
    note = input("Enter the note: ")
    msg.append(note)
    return msg
