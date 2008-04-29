#!/usr/bin/env python

from xmlparser import AlbumXMLParser
import asyncore, socket

# from twisted.internet.protocol import Protocol, ClientFactory
# from twisted.protocols.basic import LineReceiver
# from twisted.internet import reactor

from utilities import ClientConfig
from http_client import XMLGetter

class Client():
	"""docstring for Client"""
	def __init__(self):
		self.servers = ClientConfig().buddylist

	def getAlbums(self, server):
		c = XMLGetter(server, '/xml')
		asyncore.loop()
		a = AlbumXMLParser(c.xml)
		a.parse()
		return a.albums


# class PXMLClient(LineReceiver):
# 	def lineReceived(self, line):
# 		print line
# 	
# 	def getAlbums(self, server):
# 		a = AlbumXMLParser("albums.xml")
# 		a.parse()
# 		return a.albums
# 	
# 	def getHelp(self):
# 		print "fetching help"
# 		self.sendLin("help")
# 	
# 
# 
# class PXMLClientFactory(ClientFactory):
# 	protocol = PXMLClient
# 	def startedConnecting(self, connector):
# 		print 'starting to connect'
# 
# 
# def main():
# 	factory = PXMLClientFactory()
# 	
# 	reactor.connectTCP("127.0.0.1", 8407, factory)
# 	reactor.run()
# 
# 
# if __name__ == "__main__":
# 	main()