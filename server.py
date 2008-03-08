#server.py

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver, FileSender
from twisted.internet import reactor

import sys
import os
import utilities

class PXMLServer(LineReceiver, FileSender):
	def connectionMade(self):
		self.transport.write('Connected to ' + self.factory.name + '\r\n')
	
	def lineReceived(self, line):
		if line == "getxml":
			self.sendFile(self.factory.filename)
		elif line.startswith("getphoto "):
			self.sendFile(line[9:])
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
			

	def sendFile(self, filename):
		try:
			if os.access(filename, os.R_OK):
				f = open(filename, 'r')
				for line in f.readlines():
					self.sendLine(line.rstrip())
			else:
				self.sendLine('DPSP 403 Forbidden\r\n')
		except IOError:
			self.sendLine('DPSP 500 Server Error\r\n')
		

class PXMLFactory(Factory):
	protocol = PXMLServer

	def __init__(self, name=None, filename=None):
		self.name = name or 'no name'
		self.filename = filename or 'albums.xml'
	


def main():
	#first load the config file
	c = utilities.Config()
		
	#get the xml
	xml = utilities.XMLGenerator(c).generate()
	f = open("albums.xml", "w");
	f.write(xml);
	f.close();
	
	#serve the xml and the files
	reactor.listenTCP(8407, PXMLFactory(sys.argv[1]))
	reactor.run()


if __name__ == "__main__":
	main()