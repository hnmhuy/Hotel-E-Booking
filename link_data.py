import json
import user
import hotel
import time
import bill

root_path = "Data/"

# Load data function


def load_full_data():
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
                temp_room_json["date_check_in"] = []
                for item in temp_room.date_check_in:
                    day = item.tm_mday
                    month = item.tm_mon
                    year = item.tm_year
                    temp_date_str = str(day) + "/" + \
                        str(month) + "/" + str(year)
                    temp_room_json["date_check_in"].append(temp_date_str)
            else:
                temp_room_json["date_check_in"] = None
            if(temp_room.date_check_out != None):
                temp_room_json["date_check_out"] = []
                for item in temp_room.date_check_out:
                    day = item.tm_mday
                    month = item.tm_mon
                    year = item.tm_year
                    temp_date_str = str(day) + "/" + \
                        str(month) + "/" + str(year)
                    temp_room_json["date_check_out"].append(temp_date_str)
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
    now = time.localtime()
    today = time.mktime(now)
    for hotel in data_hotel:
        for room in hotel.list_room:
            if(room.user_book != None):
                i = 0
                while i < len(room.user_book):
                    if(time.mktime(room.date_check_out[i]) < today):
                        print(i)
                        room.user_book.remove(room.user_book[i])
                        room.date_check_in.remove(room.date_check_in[i])
                        room.date_check_out.remove(room.date_check_out[i])
                        continue

                    i += 1

    save_hotel_data(root_path + "/Hotel/Hotel_Data.json",
                    data_hotel, len(data_hotel))

# USER FUNCTIOS


def update_bill_in_user(user_name, new_bill_id, data_user):
    for user in data_user:
        if(user["username"] == user_name):
            user["bill"].append(new_bill_id)
            break
    save_data_user(data_user)


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
    '''
    This function does not work for bills.
    I need to update that in the future lmao ;v 
    '''

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
    '''
    user_list is a list of dictionaries
    '''

    user_data = {"users": user_list}

    json_data = json.dumps(user_data, indent=4)

    file = open("Data/User.json", "w")
    file.write(json_data)

    file.close()

    return True


def user_unit_test():
    if (user.User.check_cvv("12")):
        print("A")
    else:
        print("B")

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
    list_of_bill = []
    for i in range(number_of_bill):
        temp_bill = bill.Bill(json_object["bill_list"][i]["cancel"], json_object["bill_list"][i]["bill_id"], json_object["bill_list"][i]["list_room_id"], json_object["bill_list"][i]["user_book"],
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
            "cancel": list_of_bill[i].cancel,
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
