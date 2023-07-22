import signal
import socket
import sys
from threading import Thread
import utils
import random
import textwrap


my_n = None
my_e = None
my_d = None
my_p = None
my_q = None


print("The program will generate the inputs which you leave empty")
try:
    my_n = int(input("Enter n: "))
except Exception as e:
    my_n = None

if my_n is not None:
    try:
        my_e = int(input("Enter e: "))
    except Exception as e:
        my_e = None
    try:
        my_d = int(input("Enter d: "))
    except Exception as e:
        my_d = None
    if my_e is None or my_d is None:
        print("LOGICAL ERROR: On entering n, you must enter e and d")
        exit(0)
else:
    try:
        my_p = int(input("Enter p: "))
    except Exception as e:
        my_p = None
    try:
        my_q = int(input("Enter q: "))
    except Exception as e:
        my_q = None
    if my_p == None:
        while True:
            my_p = random.randint(10000000000000000000000000000000000,
                                  1000000000000000000000000000000000000)
            if utils.is_prime(my_p):
                break
    if my_q == None:
        while True:
            my_q = random.randint(10000000000000000000000000000000000,
                                  1000000000000000000000000000000000000)
            if utils.is_prime(my_q):
                break
    my_n = my_p * my_q

    try:
        my_e = int(input("Enter e: "))
    except Exception as e:
        my_e = None

    if my_e == None:
        try:
            my_d = int(input("Enter d: "))
        except Exception as e:
            my_d = None

    if my_e == None and my_d == None:
        while True:
            my_e = random.randint(7,
                                  7000000)
            if utils.is_prime(my_e):
                break
        my_d = utils.CalcPrivateKey(my_p, my_q, my_e)
    elif my_e == None:
        my_e = utils.CalcPrivateKey(my_p, my_q, my_d)
    elif my_d == None:
        my_d = utils.CalcPrivateKey(my_p, my_q, my_e)

    print("Current keys:")
    print("n: " + str(my_n))
    print("e: " + str(my_e))
    print("d: " + str(my_d))

print("")
print("")
print("Chat:")
print("")

Host = "localhost"
Port = 5000
MODE = 'server'
conn = None
server = None


def signal_handler(sig, frame):
    conn.close()
    if MODE == 'server':
        server.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((Host, Port))
    server.listen(1)
except Exception as e:
    MODE = 'client'
    server.connect((Host, Port))

if MODE == 'server':
    conn, _ = server.accept()
else:
    conn = server


conn.send(bytes(f"key, {my_n}, {my_e}", "utf-8"))
other_key = conn.recv(2048)
other_key = other_key.decode("utf-8")
other_key = other_key.split(',')
other_n = int(other_key[1])
other_e = int(other_key[2])


def send():
    while True:
        message = input()
        message = utils.encrypt_long_message(message, other_n, other_e)
        conn.send(bytes(message, "utf-8"))


def receive():
    while True:
        message = conn.recv(3048)
        if message == b'':
            conn.close()
            exit(0)
        message = message.decode("utf-8")
        message = utils.decrypt_long_message(message, my_n, my_d)
        print("Received> "+message)


thread = Thread(target=send)
thread.daemon = True
thread.start()

receive()
