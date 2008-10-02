#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncore, socket
from xmlparser import AlbumXMLParser
import urllib

class HTTPGetter(asyncore.dispatcher):
	"""
		Simple HTTP Client that grabs the file requested
	"""
	def __init__(self, host, path):
		""" Constructor: requires host and path. Always connect to port 8407 """
		self.data_buffer = []
		self.data = ""
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, 8407) )
		self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % urllib.pathname2url(path)
	
	def handle_connect(self):
		pass
	
	def handle_close(self):
		""" Event handler for finishing up the connection. Strips the HTTP header and save only the data """
		self.data = ''.join(self.data_buffer)
		a,b,self.data = self.data.partition("\r\n\r\n")
		self.close()
	
	def handle_read(self):
		""" Event handler for reading the file from HTTP server. Reads 8192 bytes from the server at a time """
		self.data_buffer.append(self.recv(8192))
	
	def writable(self):
		return (len(self.buffer) > 0)
	
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
	
