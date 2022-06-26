import link_data


class Room:
    def __init__(self, room_id, room_type, room_price, room_availability, user_book, date_check_int, date_check_out, decription, image_path):
        self.room_id = room_id
        self.room_type = room_type
        self.room_price = room_price
        self.room_availability = room_availability
        self.user_book = user_book
        self.date_check_int = date_check_int
        self.date_check_out = date_check_out
        self.decription = decription
        self.image_path = image_path


class Hotel:
    def __init__(self, hotel_id, hotel_name, hotel_address, number_available_room, list_room):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.hotel_address = hotel_address
        self.number_available_room = number_available_room
        self.list_room = list_room  # We will store the list of room id
