#!/usr/bin/env python

import socket

from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		self.wfile.write("<html><body><h1>hi!</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		print ("POST DATA")
		print (post_data)

		address = ('52.39.36.22', 5000)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(2)

		try:
			s.connect(address)
		except:
			print("Unable to connect")

		s.send(post_data)
		s.close()
		self._set_headers()
		self.wfile.write("{\"key\" : \"valeu\"}")


def run(server_class=HTTPServer, handler_class=S, port=8000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print ('Starting httpd...')
	httpd.serve_forever()


if __name__ == "__main__":
	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()

