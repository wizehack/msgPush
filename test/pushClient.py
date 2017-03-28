import socket
import select
import sys

def testPrompt():
	sys.stdout.write('<input msg> ')
	sys.stdout.flush()

if __name__ == "__main__":
	server_address = ('52.39.36.22', 5000)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect(server_address)
	except:
		print("Unable to connect")
		sys.exit()

	testPrompt()

	while True:
		socket_list = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			# incoming message from server
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print ("\nDisconnected from server")
					sys.exit()
				else:
					sys.stdout.write(data)
					testPrompt()
			else :
				msg = sys.stdin.readline()
				s.send(msg)
				testPrompt()
