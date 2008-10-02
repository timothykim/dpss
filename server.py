#!/usr/bin/python
"""
	DPSP Server
	
	Please refer to the final report for protocol specifications
"""
#server.py

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver, FileSender
from twisted.internet import reactor


import sys
import os
import utilities
import socket


class PXMLServer(LineReceiver, FileSender):
	""" Main Server Class """
	def connectionMade(self):
		""" Event handler for client connection. """
		self.transport.write('Connected to ' + self.factory.name + '\r\n')
		print 'Connection made.'
	
	
	def lineReceived(self, line):
		""" Parses the client requests and write out approperiate response """
		if line == "getxml":
			self.sendXML(self.factory.xml)
		elif line.startswith("getphoto "):
			self.sendPicture(line[9:])
		elif line == "quit":
			self.transport.write("good bye\r\n")
			self.transport.loseConnection()
		elif line == "help":
			self.transport.write("getxml              : get the xml file with album/photo data\r\n")
			self.transport.write("getphoto [filename] : get the photo of your choice \r\n")
			self.transport.write("help                : see this message\r\n")
			self.transport.write("quit                : disconnect\r\n")
		else:
			self.transport.write("DPSP 400 Bad Request\r\n")
	
	
	def sendXML(self, filename):
		""" Opens the specified xml file and sends it over TCP """
		try:
			f = open(filename, 'r')
			for line in f.readlines():
				self.sendLine(line.rstrip())
					
		except IOError, (errno, strerror):
			if errno == 13:
				self.sendLine('DPSP 403 Forbidden\r\n')
			elif errno == 2:
				self.sendLine('DPSP 404 Not Found\r\n')
		except:
			self.sendLine('DPSP 500 Server Error\r\n')
	
	
	def sendPicture(self, picture):
		""" Opens the specified picture file and sends it over TCP """
		try:
			re = re.compile("^" + self.libpath + "/.*\.jpe?g$")
			if not re_jpeg.match(picture.lower()):
				self.sendLine('DPSP 400 Bad Request\r\n')
				return
			
			#somehow send the binary file
			#f = open(filename, 'r')
			
			
			
		except IOError, (errno, strerror):
			if errno == 13:
				self.sendLine('DPSP 403 Forbidden\r\n')
			elif errno == 2:
				self.sendLine('DPSP 404 Not Found\r\n')
		except:
			self.sendLine('DPSP 500 Server Error\r\n')
	


class PXMLFactory(Factory):
	""" Server Factory """
	protocol = PXMLServer
	
	def __init__(self, name=None, xml=None):
		self.name = name or 'no name'
		self.xml = xml or 'albums.xml'
	


def main():
	#first load the config file
	c = utilities.Config()
	
	#get the xml
	xml = utilities.XMLGenerator(c).generate()
	f = open("albums.xml", "w");
	f.write(xml);
	f.close();
	
	#serve the xml and the files
	servername = socket.gethostname()
	
	reactor.listenTCP(8407, PXMLFactory())
	reactor.run()
	



if __name__ == "__main__":
	main()