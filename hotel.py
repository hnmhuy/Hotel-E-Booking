import link_data
import time


class Room:
    def __init__(self, room_id, room_type, room_price, room_availability, user_book, date_check_in, date_check_out, description, image_path):
        self.room_id = room_id
        self.room_type = room_type
        self.room_price = room_price
        self.room_availability = room_availability
        self.user_book = user_book
        if date_check_in != None:
            self.date_check_in = time.strptime(self.date_check_in, "%d/%m/%Y")
        else:
            self.date_check_in = None
        if date_check_out != None:
            self.date_check_out = time.strptime(
                self.date_check_out, "%d/%m/%Y")
        else:
            self.date_check_out = None
        self.description = description
        self.image_path = image_path

    def create_room_id(hotel_id, room_number, room_type):
        return hotel_id + '_' + str(room_number) + room_type[0]

    def print_room(self):
        print('-'*10)
        print('Room ID: ' + str(self.room_id))
        print('Room type: ' + str(self.room_type))
        print('Room price: ' + str(self.room_price))
        print('Room description: ' + str(self.description))
        print('-'*10)
        print('\n')

    def check_availability(self, date):
        if date >= self.date_check_in and date <= self.date_check_out:
            return False
        else:
            return True


class Hotel:
    def __init__(self, hotel_id, hotel_name, hotel_address, number_available_room):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.hotel_address = hotel_address
        self.number_available_room = number_available_room
        self.list_room = []

    def create_hotel_id(number_of_hotel):
        return "H" + str(number_of_hotel)

    def print_hotel_info(self):
        print('-'*10)
        print("Hotel ID: " + str(self.hotel_id))
        print("Hotel name: " + str(self.hotel_name))
        print("Hotel address: " + str(self.hotel_address))

    def print_list_room(self):
        for room in self.list_room:
            room.print_room()

    def print_available_room(self):
        for room in self.list_room:
            if room.room_availability == True:
                room.print_room()


def ret_hotel_id(hotel_name, hotel_list):
    for hotel in hotel_list:
        if hotel.hotel_name == hotel_name:
            return hotel.hotel_id
    return None


def find_hotel_by_id(hotel_data, hotel_id):
    for hotel in hotel_data:
        if hotel.hotel_id == hotel_id:
            return hotel
    return None


def find_room_by_id(hotel_data, room_id):
    for room in hotel_data.list_room:
        if room.room_id == room_id:
            return room
