import link_data


class Bill:
    def __init__(self, bill_id, list_room_id, user_book, time_book, total_price):
        self.bill_id = bill_id
        self.list_room_id = list_room_id
        self.user_book = user_book
        self.time_book = time_book
        self.total_price = total_price
