from numpy import number
import user
import hotel
import user
import bill

import link_data
import time

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

    if(count_available_room < number_of_room):
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
            if(count_available_room == number_of_room):
                break

        # Create a bill
        print(bill.Bill.create_bill(chosen_hotel,
              list_of_room_id, info_booking[0], data_bill)[0])

    # Update json file
    link_data.save_hotel_data(hotel_path, data_hotel, len(data_hotel))
    link_data.save_bill_data(bill_path, data_bill, len(data_bill))
    return ["Success", data_bill[len(data_bill)-1]]
