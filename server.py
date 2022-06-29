import socket
import time
# Below are the libraries used to manage data
import link_data
import hotel
import user
import bill


def main():

    # You can wirte the functions for socket here

    # Here is used to test functions in link_data.py
    # Load hotel data from file
    root_path = "Data/"
    file_path = root_path + "/Hotel/Hotel_Data.json"
    hotel_data = link_data.convert_json_to_class_hotel(
        link_data.read_hotel_data(file_path))


if __name__ == "__main__":
    main()
