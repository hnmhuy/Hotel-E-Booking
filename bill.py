import time
import datetime
import hotel


def calculate_date(date_check_in, date_check_out):
    date_start = datetime.date(
        date_check_in.tm_year, date_check_in.tm_mon, date_check_in.tm_mday)
    date_end = datetime.date(date_check_out.tm_year,
                             date_check_out.tm_mon, date_check_out.tm_mday)
    return (date_end - date_start).days


class Bill:
    def __init__(self, bill_id, list_room_id, user_book, time_book, total_price):
        self.bill_id = bill_id
        self.list_room_id = list_room_id
        self.user_book = user_book
        self.time_book = time_book
        self.total_price = total_price
        self.list_room = []

    def load_room_data_from_data_base(self, hotel_data):
        for room_id in self.list_room_id:
            self.list_room.append(hotel.find_room_by_id(hotel_data, room_id))

    def create_bill_id(hotel_id, number_of_bill):
        return "B" + str(hotel_id) + "_" + str(number_of_bill)

    def calculate_room_price(room_data):
        if(room_data.date_check_in != None and room_data.date_check_out != None):
            day_diff = calculate_date(
                room_data.date_check_in[len(room_data.date_check_in)-1],
                room_data.date_check_out[len(room_data.date_check_out)-1])
            return day_diff * room_data.room_price
        else:
            return -1

    def calculate_total_price(hotel_data, list_room_id):
        total_price = 0
        flag = False
        for room_id in list_room_id:
            room_data = hotel.find_room_by_id(hotel_data, room_id)
            room_price = Bill.calculate_room_price(room_data)
            if room_price == -1:
                flag = True
                break
            else:
                total_price += room_price

        if flag == True:
            return -1
        else:
            return total_price

    def create_bill(hotel_data, list_room_id, user_book, list_of_bill):
        total_price = Bill.calculate_total_price(hotel_data, list_room_id)
        if total_price == -1:
            return False
        else:
            bill_id = Bill.create_bill_id(
                hotel_data.hotel_id, len(list_of_bill)+1)
            now = time.time()
            time_book = time.strftime("%H:%M:%S %d/%m/%Y")
            bill = Bill(bill_id, list_room_id, user_book,
                        time_book, total_price)
            bill.load_room_data_from_data_base(hotel_data)
            list_of_bill.append(bill)

            return ["Bill created successfully", True]

    def available_to_cancel(self):
        # This bill is available to cancle if time_book < 24 hours
        time_book = time.strptime(self.time_book, "%H:%M:%S %d/%m/%Y")
        time_book = datetime.datetime(time_book.tm_year, time_book.tm_mon,
                                      time_book.tm_mday, time_book.tm_hour, time_book.tm_min, time_book.tm_sec)
        time_now = datetime.datetime.now()
        delta = time_now - time_book
        if delta.days == 0:
            if delta.seconds < 86400:
                return True
        return False

    def cancel_bill(bill_id, list_of_bill):
        for bill in list_of_bill:
            if bill.bill_id == bill_id:
                list_of_bill.remove(bill)
                return True
        return False


def find_bill_by_id(list_of_bill, id):
    for bill in list_of_bill:
        if bill.bill_id == id:
            return bill
    return None

def find_bill_by_user(list_of_bill, user):
    for bill in list_of_bill:
        if bill.user_book == user:
            return bill
    return None

def print_bill(bill):
    print('_'*30)
    print("YOUR BILL WAS CREATED SUCCESSFULLY")
    print('_'*30)
    print("Bill ID: ", bill.bill_id)
    print("User book: ", bill.user_book)
    print("Time book: ", bill.time_book)
    print("_"*30)
    print("List room: ")
    print("_"*30)
    count = 0
    index_user_in_bill = 0
    for i in range(len(bill.list_room[0].user_book)):
        if bill.user_book == bill.list_room[0].user_book[i]:
            index_user_in_bill = i
            break
    for room in bill.list_room:
        if(room is not None):
            count += 1
            print(' '*10 + "Room "+str(count)+" "*11)
            print(f"Room ID:        {room.room_id}")
            print(f"Room type:      {room.room_type}")
            print(
                f"Room check in:  {room.date_check_in[index_user_in_bill].tm_mday}/{room.date_check_in[index_user_in_bill].tm_mon}/{room.date_check_in[index_user_in_bill].tm_year}")
            print(
                f"Room check out: {room.date_check_out[index_user_in_bill].tm_mday}/{room.date_check_out[index_user_in_bill].tm_mon}/{room.date_check_out[index_user_in_bill].tm_year}")
            print(
                f"Room price:     {room.room_price} x {calculate_date(room.date_check_in[index_user_in_bill], room.date_check_out[index_user_in_bill])}")
            print("-"*20)
            print(f"{Bill.calculate_room_price(room)}")
            print("_"*30)

    print("Total price: ", bill.total_price)
