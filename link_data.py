import json
import user
import hotel
from bill import Bill
import time
import bill

root_path = "Data/"

# Load data function


def load_full_data():
    '''
    Return a list of data
    data[0] = list of hotel
    data[1] = number of hotel
    data[2] = list of user
    data[3] = list of bill
    data[4] = number of bill
    '''
    data = []
    # Load hotel data
    hotel_data = []
    hotel_data = convert_json_to_class_hotel(
        read_hotel_data(root_path + "/Hotel/Hotel_Data.json"))
    data.append(hotel_data)
    data.append(len(hotel_data))
    # Load user data
    user_data = []
    user_data = load_data_user()
    data.append(user_data)
    # Load bill data
    bill_data = []
    bill_data = convert_json_to_class_bill(
        load_data_bill_json(root_path + "/Bill.json"))
    data.append(bill_data)
    data.append(len(bill_data))
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
    json_object = {}
    json_object["number_of_hotel"] = number_of_hotel
    json_object["hotel"] = []
    for i in range(number_of_hotel):
        temp_hotel = list_of_hotel[i]
        temp_hotel_json = {}
        temp_hotel_json["hotel_id"] = temp_hotel.hotel_id
        temp_hotel_json["hotel_name"] = temp_hotel.hotel_name
        temp_hotel_json["hotel_address"] = temp_hotel.hotel_address
        temp_hotel_json["number_available_room"] = temp_hotel.number_available_room
        temp_hotel_json["room"] = []
        for j in range(len(temp_hotel.list_room)):
            temp_room = temp_hotel.list_room[j]
            temp_room_json = {}
            temp_room_json["room_id"] = temp_room.room_id
            temp_room_json["room_type"] = temp_room.room_type
            temp_room_json["room_price"] = temp_room.room_price
            temp_room_json["room_availability"] = temp_room.room_availability
            temp_room_json["user_book"] = temp_room.user_book
            if(temp_room.date_check_in != None):
                day = temp_room.date_check_in.tm_mday
                month = temp_room.date_check_in.tm_mon
                year = temp_room.date_check_in.tm_year
                temp_room_json["date_check_in"] = str(
                    day) + "/" + str(month) + "/" + str(year)
            else:
                temp_room_json["date_check_in"] = None
            if(temp_room.date_check_out != None):
                day = temp_room.date_check_out.tm_mday
                month = temp_room.date_check_out.tm_mon
                year = temp_room.date_check_out.tm_year
                temp_room_json["date_check_out"] = str(
                    day) + "/" + str(month) + "/" + str(year)
            else:
                temp_room_json["date_check_out"] = None
            temp_room_json["description"] = temp_room.description
            temp_room_json["image_path"] = temp_room.image_path
            temp_hotel_json["room"].append(temp_room_json)
        json_object["hotel"].append(temp_hotel_json)
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


def auto_update_room_status(data_hotel):
    today = time.time()
    for hotel in data_hotel:
        for room in hotel.list_room:
            if(room.date_check_in == None and room.date_check_out == None):
                continue
            else:
                # Check today is in range of date_check_in and date_check_out
                if(today >= time.mktime(room.date_check_in) and today <= time.mktime(room.date_check_out)):
                    room.room_availability = False
                else:
                    room.room_availability = True
                    room.date_check_in = None
                    room.date_check_out = None
                    room.user_book = None

    save_hotel_data(root_path + "/Hotel/Hotel_Data.json",
                    data_hotel, len(data_hotel))

# USER FUNCTIOS


def load_data_user():
    '''
    This function returns a list of users
    in the database as a list of dictionaries
    '''

    data = open("Data/User.json")
    json_object = json.load(data)
    data.close()

    return json_object["users"]


def change_user_data(username, target_key, change_value):
    file = open("Data/User.json")
    json_object = json.load(file)

    found = False

    for find_user in json_object["users"]:
        if find_user["username"] == username:
            find_user[target_key] = change_value
            found = True
            break

    file.close()

    if not found:
        return False

    new_data = json.dumps(json_object, indent=4)

    file = open("Data/User.json", "w")
    file.write(new_data)

    return True


def save_data_user(user_list):
    user_data = {"users": user_list}

    json_data = json.dumps(user_data, indent=4)

    file = open("Data/User.json", "w")
    file.write(json_data)

    file.close()

    return True


def user_unit_test():
    # new_user = user.User.create_new_user()
    # profile = load_data_user("deeznuts")

    # print(new_user.username)
    # print(profile.password)

    # DATA USE FOR TESTING ONLY
    # user_list = [
    #     {
    #         "fullname": "John Doe",
    #         "birthday": "01/01/1970",
    #         "username": "jdoe",
    #         "password": "jdoe",
    #         "credit_card": "123456789",
    #         "cvv": "666",
    #         "expiration_date": "01/2020",
    #         "bill": []
    #     },
    #     {
    #         "fullname": "Coin Card",
    #         "birthday": "19/12/2003",
    #         "username": "yeee",
    #         "password": "deeznuts",
    #         "credit_card": "123456789",
    #         "cvv": "666",
    #         "expiration_date": "01/2024",
    #         "bill": []
    #     },
    #     {
    #         "fullname": "Leroy Jenkins",
    #         "birthday": "6/9/1969",
    #         "username": "deeznuts",
    #         "password": "bruhbruhlmao",
    #         "credit_card": "1234123412",
    #         "cvv": "123",
    #         "expiration_date": "06/2025"
    #     }
    # ]

    # save_data_user(user_list)

    # user_list = load_data_user()
    # print(user_list)

    if change_user_data("deeznuts", "cvv", "420"):
        print("Success")
    else:
        print("Failed")

# BILL FUNCTIONS


def load_data_bill_json(file_path):
    data = open(file_path)
    try:
        json_object = json.load(data)
    except:
        json_object = {}
    data.close()
    return json_object


def convert_json_to_class_bill(json_object):
    if json_object == {}:
        return []
    number_of_bill = int(json_object["number_of_bill"])
    if number_of_bill == 0:
        return None
    list_of_bill = []
    for i in range(number_of_bill):
        temp_bill = Bill(json_object["bill_list"][i]["bill_id"], json_object["bill_list"][i]["list_room_id"], json_object["bill_list"][i]["user_book"],
                         json_object["bill_list"][i]["time_book"], json_object["bill_list"][i]["total_price"])
        list_of_bill.append(temp_bill)
    return list_of_bill


def convert_class_bill_to_json(list_of_bill, number_of_bill):
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
    return json.dumps(json_object, indent=4)


def save_bill_data(file_path, list_of_bill, number_of_bill):
    json_object = convert_class_bill_to_json(list_of_bill, number_of_bill)
    with open(file_path, "w") as json_file:
        json_file.write(json_object)
    json_file.close()

# def main():

#     # Unit test for user
#     user_unit_test()


# if __name__ == "__main__":
#     main()
