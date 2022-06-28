from sys import flags
import link_data
import time
import datetime


class Bill:
    def __init__(self, bill_id, list_room_id, user_book, time_book, total_price):
        self.bill_id = bill_id
        self.list_room_id = list_room_id
        self.user_book = user_book
        self.time_book = time_book
        self.total_price = total_price

    def create_bill_id(hotel_id, number_of_bill):
        return "B" + str(hotel_id) + str(number_of_bill)

    def calculate_room_price(hotel_data, room_id):
        room_data = link_data.find_room_by_id(hotel_data, room_id)
        if(room_data.date_check_in != None and room_data.date_check_out != None):
            delta = room_data.date_check_out - room_data.date_check_in
            return delta.days * room_data.room_price
        else:
            return -1

    def calculate_total_price(hotel_data, list_room_id):
        total_price = 0
        flag = False
        for room_id in list_room_id:
            temp = Bill.calculate_room_price(hotel_data, room_id)
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
            return "Something went wrong, one or more room don't available"
        else:
            bill_id = Bill.create_bill_id(
                hotel_data.hotel_id, list_of_bill.len()+1)
            time_book = time.strftime(time.time(), "%H:%M:%S %d/%m/%Y")
            bill = Bill(bill_id, list_room_id, user_book,
                        time_book, total_price)
            list_of_bill.append(bill)
            return "Bill created successfully"
