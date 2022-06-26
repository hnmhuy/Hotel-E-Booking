import link_data


class User:
    def __init__(self, fullname, birthdate, username, password, credit_card, cvv, expiration_data):
        self.fullname = fullname  # string
        self.birthdate = birthdate  # string
        self.username = username  # string, maximum length = 32
        # string, lowercase, uppercase, number, special character, minimum length = 4
        self.password = password
        self.credit_card = credit_card
        self.cvv = cvv  # 3 or 4 digits
        self.expiration_data = expiration_data

    def get_full_name(self):
        return self.fullname

    def get_birthdate(self):
        return self.birthdate

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_credit_card(self):
        return self.credit_card

    def get_cvv(self):
        return self.cvv

    def get_expiration_data(self):
        return self.expiration_data


def get_info_user(username):
    return None


def check_format_date(date):
    return True


def check_user_name(username):
    return True


def check_password(password):
    return True


def check_credit_card(credit_card):
    return True


def check_cvv(cvv):
    return True


def check_expiration_data(expiration_data):
    return True


def create_new_user(fullname, birthdate, username, password, credit_card, cvv, expiration_data):
    return None
