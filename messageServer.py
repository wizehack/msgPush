# server

import socket
import select

def broadcast_data (sock, message):
	for socket in CONNECTION_LIST:
		if socket != server_socket and socket != sock :
			try:
				socket.send(message)
			except:
				socket.close()
				CONNECTION_LIST.remove(socket)


def process_cmd_data (data):
	# parse api.ai response
	return data


if __name__ == "__main__":
	CONNECTION_LIST = []
	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	PORT = 5000

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)

	# Add server socket to the list of readable
	# connections
	CONNECTION_LIST.append(server_socket)
	print("Chat server started on port " + str(PORT))

	while True:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

		for sock in read_sockets:
			#New connection
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print("Client (%s, %s) connected" % addr)
			else: #Some incoming message from a client
				try:
					data = sock.recv(RECV_BUFFER)
					if data:
						broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + process_cmd_data(data))
				except:
					broadcast_data(sock, "Client (%s, %s) is offline" % addr)
					print("Client (%s, %s) is offline" % addr)
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue

	server_socket.close()
