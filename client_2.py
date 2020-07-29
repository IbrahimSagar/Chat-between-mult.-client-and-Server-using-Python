import socket
import select
import errno   #for error
import sys

HeaderSize = 10
IP = "localhost"
PORT = 1235

my_username = input("Username: ")
client = socket.socket()
client.connect((IP,PORT))
client.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HeaderSize}}".encode('utf-8')
client.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    #false enter or false msg check
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HeaderSize}}".encode('utf-8')
        client.send(message_header + message)

    try:
        while True:
            #receive things
            username_header = client.recv(HeaderSize)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client.recv(username_length).decode('utf-8')

            message_header = client.recv(HeaderSize)
            message_length = int(message_header.decode('utf-8').strip())
            message = client.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error",str(e))
            sys.exit()
        continue

    except Exception as e:
        print('general error',str(e))
        sys.exit()

