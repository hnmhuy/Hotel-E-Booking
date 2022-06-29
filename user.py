# import link_data

class User:
    def __init__(self, fullname, birthday, username, password, credit_card, cvv, expiration_data):
        self.fullname = fullname    # string
        self.birthday = birthday  # string
        self.username = username    # string, maximum length = 32

        # string, lowercase, uppercase, number, special character, minimum length = 4
        self.password = password

        self.credit_card = credit_card
        self.cvv = cvv  # 3 or 4 digits
        self.expiration_data = expiration_data
