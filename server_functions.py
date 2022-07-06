import hotel
import user
import bill

import link_data
import server


def find_available_rooms(hotel):
    room_count = 0
    room_list = []

    if hotel.number_available_room == 0:
        return room_count, room_list 

    for room in hotel.list_room:
        if room.room_availability == True:
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

            number_of_rooms, found_rooms = find_available_rooms(hotel)
            break

    return number_of_rooms, found_rooms