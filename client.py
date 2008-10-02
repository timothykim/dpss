#!/usr/bin/env python
"""
	Client Module
	
	Makes connections to the DPSP server to retireive necessary files
"""
from xmlparser import AlbumXMLParser
import asyncore, socket


from utilities import ClientConfig
from http_client import HTTPGetter
from urllib import urlretrieve, quote
import hashlib 
import os

class Client():
	"""
	This is the 'Client' class
	
	It is uses http to establish connections with DPSP server and download necessary files. For example,
	
	>>> c = Client()
	>>> c.getAlbums("127.0.0.1")
	[{ 'name': 'album1', 'count': 1, 'photos': [{'path': '/path/to/photo', 'thumb': '/path/to/thumbnail'}] }]
	
	"""
	def __init__(self):
		""" Constructor, requires ClientConfig classs """
		self.servers = ClientConfig().buddylist

	def getAlbums(self, server):
		""" Retreives the album data from the specified server """
		try:
			xml = HTTPGetter(server, '/xml')
			asyncore.loop()
			a = AlbumXMLParser(xml.data)
			a.parse()
			return a.albums
		except Exception, e:
			return []
	
	
	def getThumb(self, server, uri):
		""" Retrieves the requested photo and saves it in a cache """
		url = 'http://' + server + ':8407/thumb' + quote(uri)
		filename = "./tmp/" + hashlib.sha1(url).hexdigest() + ".jpg"
		if not os.path.exists(filename):
			urlretrieve(url, filename)
		return filename
	
	def getOriginal(self, server, uri):
		""" Retrieves the requested photo and saves it in a cache """
		url = 'http://' + server + ':8407/original' + quote(uri)
		filename = "./tmp/" + hashlib.sha1(url).hexdigest() + ".jpg"
		if not os.path.exists(filename):
			urlretrieve(url, filename)
		return filename
	

