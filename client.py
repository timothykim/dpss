#!/usr/bin/env python

from xmlparser import AlbumXMLParser

class Client():
	
	servers = ["Tim's Computer"]
	
	"""docstring for Client"""
	def __init__(self):
		pass
		
	
	def getAlbums(self, server):
		a = AlbumXMLParser("albums.xml")
		a.parse()
		return a.albums
		
		
	def connect(self, ip):
		self.current_server = ip
		return true;

