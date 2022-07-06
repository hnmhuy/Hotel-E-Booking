import hotel
import user
import bill

import time

import link_data
import server


def find_available_rooms(hotel, user_check_in, user_check_out):
    room_count = 0
    room_list = []

    user_check_in = user_check_in + " 13:00:00"
    user_check_out = user_check_out + " 12:00:00"

    user_start = time.strptime(user_check_in, "%d/%m/%Y %H:%M:%S")
    user_end = time.strptime(user_check_out, "%d/%m/%Y %H:%M:%S")

    if hotel.number_available_room == 0:
        return room_count, room_list 

    for room in hotel.list_room:

        if (room.room_availability == True or (room.room_availability == False and
            ((time.mktime(user_start) < time.mktime(room.date_check_in) and time.mktime(user_end) < time.mktime(room.date_check_in)) or
            (time.mktime(user_start) > time.mktime(room.date_check_out) and time.mktime(user_end) > time.mktime(room.date_check_out))))):

            room_count += 1
            room_list.append(room)

    return room_count, room_list


def search_hotel(target_hotel, hotel_list):
    '''
    target_hotel = {
        "name": "HOTEL NAME",
        "check_in": "DD/MM/YYYY",
        "check_out": "DD/MM/YYYY",
        "room_type": "ROOM_TYPE"    # Not sure if
                                    # this is required
    }
    '''

    number_of_rooms = 0
    found_rooms = []
    
    for hotel in hotel_list:
        current_name = hotel.hotel_name.lower()
        target = target_hotel["name"].lower()

        if (current_name == target or
                current_name.replace(" ", "") in target.replace(" ", "") or
                target.replace(" ", "") in current_name.replace(" ", "")):

            number_of_rooms, found_rooms = find_available_rooms(hotel, target_hotel["check_in"],
                                                                    target_hotel["check_out"])
            break

    return number_of_rooms, found_rooms