"""
	Client side of the chat room

	Usage:
	python ./lanchat.py IPAddress PortNumber

	Ref: https://www.geeksforgeeks.org/simple-chat-room-using-python/

"""
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
	print "Please enter: script, IP address, port number"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.connect((IP_address, Port))

while True:

	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks != server:
			message = sys.stdin.readline()
			server.send(message)
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()
		else:
			message = socks.recv(2048)
			print message

server.close()
