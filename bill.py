import link_data
import time
import datetime
import hotel


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
            delta = room_data.date_check_out - room_data.date_check_in
            return delta.days * room_data.room_price
        else:
            return -1

    def calculate_total_price(self):
        total_price = 0
        flag = False
        for room in self.list_room:
            temp = Bill.calculate_room_price(room)
            if temp != -1:
                total_price += temp
            else:
                flag = True
                break
        if flag:
            return -1
        else:
            return total_price

    def create_bill(hotel_data, list_room_id, user_book, time_book, list_of_bill):
        total_price = Bill.calculate_total_price(hotel_data, list_room_id)
        if total_price == -1:
            return ["Something went wrong, one or more room don't available", False]
        else:
            bill_id = Bill.create_bill_id(
                hotel_data.hotel_id, list_of_bill.len()+1)
            time_book = time.strftime(time.time(), "%H:%M:%S %d/%m/%Y")
            bill = Bill(bill_id, list_room_id, user_book,
                        time_book, total_price)
            list_of_bill.append(bill)
            return ["Bill created successfully", True]

    def available_to_cancle(self):
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

    def cancle_bill(hotel_data, bill_id, list_of_bill):
        for bill in list_of_bill:
            if bill.bill_id == bill_id:
                list_of_bill.remove(bill)
                return ["Bill cancled successfully", True]
        return ["Bill not found", False]


def find_bill_by_id(list_of_bill, id):
    for bill in list_of_bill:
        if bill.bill_id == id:
            return bill
    return None


def print_bill(bill):
    print('_'*20)
    print("YOUR BILL WAS CREATED SUCCESSFULLY")
    print('_'*20)
    print("Bill ID: ", bill.bill_id)
    print("User book: ", bill.user_book)
    print("Time book: ", bill.time_book)
    print("_"*20)
    print("List room: ")
    for room in bill.list_room:
        print(f"Room ID:        {room.room_id}")
        print(f"Room type:      {room.room_type}")
        print(f"Room check in:  {room.date_check_in}")
        print(f"Room check out: {room.date_check_out}")
        print(
            f"Room price:     {room.room_price} x {room.date_check_out - room.date_check_in})")
        print("-"*10)
        print(f"Total price:    {Bill.calculate_room_price(room)}")
        print("_"*20)
