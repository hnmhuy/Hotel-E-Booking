import socket
from PIL import Image
import pickle
import sys

from server import BUFFER_IMG

HOST = "127.0.0.1"
SERVER_PORT = 65500
FORMAT = "utf8"
BUFFER_IMG = 4096


def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        # wait response
        client.recv(1024)

    msg = "end"
    client.send(msg.encode(FORMAT))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")


try:
    client.connect((HOST, SERVER_PORT))
    print("client address:", client.getsockname())
    print("client:", HOST, SERVER_PORT)
    print("Connected to server")
    reply = client.recv(1024).decode(FORMAT)
    print("reply:", reply)
    msg = None
    while (msg != "x"):
        user_info = ["benn", "122345", "end"]
        sendList(client, user_info)
        print("user_info:", user_info)
        print("Received:", client.recv(1024).decode(FORMAT))
        # msg = input("talk: ")
        # client.sendall(msg.encode(FORMAT))
        # if (msg == "list"):
        #     # wait response
        #     client.recv(1024)
        #     sendList(client, list)
        # elif (msg == "img"):
        #     # Receive the number of packet
        #     num_packet = int(client.recv(1024).decode(FORMAT))
        #     print("num_packet:", num_packet)
        #     with open("test.jpg", "wb") as f:
        #         for i in range(num_packet):
        #             data = client.recv(BUFFER_IMG)
        #             f.write(data)
        #     f.close()
        # Ask to see the image
        # print("Do you want to see the image? (y/n)")
        # answer = input()
        # if (answer == "y"):
        #     img = Image.open("test.jpg")
        #     img.show()
        # else:
        #     print("Image is not shown")


except:
    print("Error")


client.close()
