"""
	Server side of the chat room

	Usage:
	python ./lanscan.py IPAddress PortNumber

	Ref: https://www.geeksforgeeks.org/simple-chat-room-using-python/

"""

import socket
import select
import sys
from thread import *

# AF_INET = address domain of the socket
# SOCK_STREAM = type of socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
list_of_clients = []

if len(sys.argv) != 3:
	print "Please enter: script, IP address, port number"
	exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)


def broadcast(message, connection):
	for client in list_of_clients:
		if client!=connection:
			try:
				client.send(message)
			except:
				client.close()
				if client in list_of_clients:
					list_of_clients.remove(client)

def clientthread(conn, addr):
	conn.send("You have entered the chatroom.")
	while True:
			try:
				message = conn.recv(2048)
				if message:
					print "<Client " + addr[0] + "> " + message
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)
				else:
					if conn in list_of_clients:
						list_of_clients.remove(conn)
			except:
				continue

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print addr[0] + " connected"
	start_new_thread(clientthread,(conn,addr)) 

conn.close()
server.close()
