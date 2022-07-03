import json
import time

import link_data


class User:
    def __init__(self, fullname, birthday, username,
                 password, credit_card, cvv, expiration_date):

        self.fullname = fullname    # string
        self.birthday = birthday    # string
        self.username = username    # string, maximum length = 32

        # string, lowercase, uppercase, number, special character, minimum length = 4
        self.password = password

        self.credit_card = credit_card
        self.cvv = cvv  # 3 or 4 digits
        self.expiration_date = expiration_date

    # def check_format_date(date):

    #     return True

    def check_username_availability(username):
        data = open("Data/User.json")
        json_object = json.load(data)

        for search_user in json_object["users"]:
            if search_user["username"] == username:
                data.close()
                return False

        data.close()
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
        if len(credit_card) != 16:
            return False

        return True

    def check_cvv(cvv):
        if (len(cvv) != 3 or len(cvv) != 4):
            return False

        return True

    def check_expiration_date(expiry_date):
        format_date = expiry_date.split("/")

        current = time.localtime()

        if int(format_date[1]) < current.tm_year:
            return False

        if (int(format_date[1]) == current.tm_year and int(format_date[0]) < current.tm_mon):
            return False

        return True

    def create_new_user():
        username = input("Enter username: ")

        while not User.check_username_availability(username):
            username = input("Username taken, please enter a new name: ")

        password = input("Enter password: ")
        while not User.check_password(password):
            password = input(
                "Password must include upper case, lower case, numbers and special characters: ")

        confirm_password = input("Re-enter password: ")

        while password != confirm_password:
            print("Password not matched! Please re-enter!")

            password = input("Enter password: ")
            while not User.check_password(password):
                password = input(
                    "Password must include upper case, lower case, numbers and special characters: ")

            confirm_password = input("Re-enter password: ")

        full_name = input("Enter full name: ")
        birthday = input("Enter birthday: ")

        card_id = input("Enter credit card number: ")
        while not User.check_credit_card(card_id):
            card_id = input("Card not available, please re-enter number: ")

        cvv = input("Enter security code: ")
        while not User.check_cvv(cvv):
            cvv = input("Wrong CVV, please re-enter: ")

        expiry_date = input("Enter expiration date: ")
        while not User.check_expiration_date(expiry_date):
            expiry_date = input("Card had expired, re-enter date: ")

        new_user = User(full_name, birthday, username,
                        password, card_id, cvv, expiry_date)

        return new_user
