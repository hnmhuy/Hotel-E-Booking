import json
import user
import hotel
from bill import Bill
import time
import bill

# Load data function


def load_full_data():
    data = []
    root_path = "Hotel/"
    # Load hotel data
    hotel_data = []
    hotel_data = convert_json_to_class_hotel(
        read_hotel_data(root_path + "/Hotel/Hotel_Data.json"))
    data.append(hotel_data)
    data.append(hotel_data.len())
    # Load bill data
    bill_data = []
    bill_data = convert_json_to_class_bill(
        load_data_bill_json(root_path + "/Bill.json"))
    data.append(bill_data)
    data.append(bill_data.len())

    return data


# Hotel functions
# These function are used to read, write and replace data of hotel in json file


def read_hotel_data(file_path):
    with open(file_path, "r") as json_file:
        json_object = json.load(json_file)
        return json_object


def get_hotel_info(list_hotel):
    number_of_hotel = 0
    request = 'y'
    while request == 'y' or request == 'Y':
        name = input("Enter hotel name: ")
        address = input("Enter hotel address: ")
        number_of_room = int(input("Enter number of room: "))
        hotel_id = hotel.Hotel.create_hotel_id(number_of_hotel)
        temp_hotel = hotel.Hotel(hotel_id, name, address, number_of_room)
        for i in range(number_of_room):
            room_type = input("Enter room type: ")
            room_price = int(input("Enter room price: "))
            room_availability = True
            user_book = None
            date_check_in = None
            date_check_out = None
            description = input("Enter description: ")
            image_path = None
            room_id = hotel.Room.create_room_id(hotel_id, i, room_type)
            temp_room = hotel.Room(room_id, room_type, room_price, room_availability,
                                   user_book, date_check_in, date_check_out, description, image_path)
            temp_hotel.list_room.append(temp_room)
        number_of_hotel += 1
        list_hotel.append(temp_hotel)
        request = input("Do you want to add more hotel? (y/n) ")
    return number_of_hotel


def convert_class_hotel_to_json(list_of_hotel, number_of_hotel):
    json_hotel = "{\"number_of_hotel\": " + \
        str(number_of_hotel) + ","+"\"hotel\": ["
    for i in range(len(list_of_hotel)):
        json_hotel += "{\"hotel_id\":" + "\"" + list_of_hotel[i].hotel_id + "\"," + "\"hotel_name\":" + "\"" + list_of_hotel[i].hotel_name + "\"," + "\"hotel_address\":" + \
            "\"" + list_of_hotel[i].hotel_address + "\"," + "\"number_available_room\":" + \
            "\"" + \
            str(list_of_hotel[i].number_available_room) + "\"," + "\"room\": ["
        for j in range(len(list_of_hotel[i].list_room)):
            json_hotel += json.dumps(list_of_hotel[i].list_room[j].__dict__)
            if j != len(list_of_hotel[i].list_room)-1:
                json_hotel += ","
        json_hotel += "]}"
        if i != len(list_of_hotel)-1:
            json_hotel += ","
    json_hotel += "]}"
    json_object = json.loads(json_hotel)
    return json.dumps(json_object, indent=4)


def convert_json_to_class_hotel(json_object):
    list_of_hotel = []
    number_of_hotel = json_object["number_of_hotel"]
    for i in range(number_of_hotel):
        hotel_id = json_object["hotel"][i]["hotel_id"]
        hotel_name = json_object["hotel"][i]["hotel_name"]
        hotel_address = json_object["hotel"][i]["hotel_address"]
        number_available_room = json_object["hotel"][i]["number_available_room"]
        temp_hotel = hotel.Hotel(hotel_id, hotel_name,
                                 hotel_address, number_available_room)
        for j in range(len(json_object["hotel"][i]["room"])):
            room_id = json_object["hotel"][i]["room"][j]["room_id"]
            room_type = json_object["hotel"][i]["room"][j]["room_type"]
            room_price = json_object["hotel"][i]["room"][j]["room_price"]
            room_availability = json_object["hotel"][i]["room"][j]["room_availability"]
            user_book = json_object["hotel"][i]["room"][j]["user_book"]
            date_check_in = json_object["hotel"][i]["room"][j]["date_check_in"]
            date_check_out = json_object["hotel"][i]["room"][j]["date_check_out"]
            description = json_object["hotel"][i]["room"][j]["description"]
            image_path = json_object["hotel"][i]["room"][j]["image_path"]
            temp_room = hotel.Room(room_id, room_type, room_price, room_availability,
                                   user_book, date_check_in, date_check_out, description, image_path)
            temp_hotel.list_room.append(temp_room)
        list_of_hotel.append(temp_hotel)
    return list_of_hotel

def save_hotel_data(file_path, list_hotel, number_of_hotel):
    json_object = convert_class_hotel_to_json(list_hotel, number_of_hotel)
    with open(file_path, "w") as json_file:
        json_file.write(json_object)
    json_file.close()


def decode_room_id(room_id):
    room_id = room_id.split("_")
    return room_id[0], room_id[1]

def find_hotel_by_id(hotel_data, hotel_id):
    for hotel in hotel_data:
        if hotel.hotel_id == hotel_id:
            return hotel
    return None


def find_room_by_id(hotel, room_id):
    for room in hotel.list_room:
        if room.room_id == room_id:
            return room
    return None

# USER FUNCTIONS

def create_new_user():
    username = input("Enter username: ")

    password = input("Enter password: ")
    confirm_password = input("Re-enter password: ")

    while password != confirm_password:
        print("Password not matched! Please re-enter!")
        password = input("Enter password: ")
        confirm_password = input("Re-enter password: ")

    full_name = input("Enter full name: ")
    birthday = input("Enter birthday: ")
    card_id = input("Enter credit card number: ")
    cvv = input("Enter security code: ")
    expiry_date = input("Enter expiration date: ")

    new_user = user.User(full_name, birthday, username,
                         password, card_id, cvv, expiry_date)

    return new_user


def load_data_user(username):
    data = open("Data/User.json")
    json_object = json.load(data)

    for find_user in json_object["users"]:
        if find_user["username"] == username:

            user_data = user.User(find_user["fullname"], find_user["birthday"],
                                  find_user["username"], find_user["password"],
                                  find_user["credit_card"], find_user["cvv"],
                                  find_user["expiration_date"])

            return user_data

    return None


def check_format_date(date):
    return True


def check_username_availability(username):
    data = open("Data/User.json")
    json_object = json.load(data)

    for search_user in json_object["users"]:
        if search_user["username"] == username:
            return False

    return True


def check_password(password):
    SPECIAL_CHARACTERS = "!@#$%^&*()-+=_"
    NUMBERS = "123456789"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER = "abcdefghijklmnopqrstuvwxyz"

    has_special_characters = False
    has_number = False
    has_upper = False
    has_lower = False

    for char in SPECIAL_CHARACTERS:
        if char in password:
            has_special_characters = True
            break

    for char in NUMBERS:
        if char in password:
            has_number = True
            break

    for char in UPPER:
        if char in password:
            has_upper = True
            break

    for char in LOWER:
        if char in password:
            has_lower = True
            break

    if (has_special_characters and has_number and
            has_upper and has_lower):
        return True

    return False


def check_credit_card(credit_card):
    return True


def check_cvv(cvv):
    return True


def check_expiration_data(expiration_data):
    return True


# def create_new_user(fullname, birthdate, username, password, credit_card, cvv, expiration_data):
#     return None


def user_unit_test():
    # new_user = create_new_user()
    # profile = load_data_user("deeznuts")

    # print(new_user.username)
    # print(profile.password)

    if check_password("Lmao@BRUH123"):
        print("NICE")
    else:
        print("NOT NICE")

    if check_username_availability("deeznuts"):
        print("AVAILABLE")
    else:
        print("NOT AVAILABLE")

# BILL FUNCTIONS


def load_data_bill_json(file_path):
    data = open(file_path)
    json_object = json.load(data)
    return json_object


def convert_json_to_class_bill(json_object):
    number_of_bill = int(json_object["number_of_bill"])
    list_of_bill = []
    for i in range(number_of_bill):
        temp_bill = Bill(json_object["bill_list"][i]["bill_id"], json_object["bill_list"][i]["list_room_id"], json_object["bill_list"][i]["user_book"],
                         json_object["bill_list"][i]["time_book"], json_object["bill_list"][i]["total_price"])
        list_of_bill.append(temp_bill)
    return list_of_bill


def covert_class_bill_to_json(list_of_bill, number_of_bill):
    json_object = {
        "number_of_bill": number_of_bill,
        "bill_list": []
    }
    for i in range(number_of_bill):
        json_object["bill_list"].append({
            "bill_id": list_of_bill[i].bill_id,
            "list_room_id": list_of_bill[i].list_room_id,
            "user_book": list_of_bill[i].user_book,
            "time_book": list_of_bill[i].time_book,
            "total_price": list_of_bill[i].total_price
        })
    return json_object


def main():
    # Unit test for user
    user_unit_test()


if __name__ == "__main__":
    main()
