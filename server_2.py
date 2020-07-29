import socket
import select

HeaderSize = 10
IP = "localhost"
PORT = 1235

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((IP, PORT))
server.listen()

socket_list = [server]

clients = {}


def receive_message(client):
    try:
        msg_header = client.recv(HeaderSize)
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode("utf-8").strip())
        return {"header":msg_header, "data":client.recv(msg_length)}
    except:
        pass

while True:
    read_sockets, _, exception_sockets = select.select(socket_list,[],socket_list) #socket read , socket write , list

    for notified_socket in read_sockets:
        if notified_socket == server:
            client,client_address = server.accept()

            user = receive_message(client)
            if user is False:
                continue
            socket_list.append(client)
            clients[client] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
        else:
            massage = receive_message(notified_socket)

            if massage is False:
                print(f"Closed connection from{clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]

            print(f"Recieved message from {user['data'].decode('utf-8') } : {massage['data'].decode('utf-8')}")
            #share msg with everybody
            for client in clients:
                if client != notified_socket:
                    client.send(user['header'] + user['data'] + massage['header'] + massage['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]