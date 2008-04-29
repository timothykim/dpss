#!/usr/bin/env python

import xml.parsers.expat


class AlbumXMLParser():

	albums = []
	current_album = {}

	def __init__(self, xml_str):
		assert(xml_str != "")

		self.xml_str = xml_str

		self.Parser = xml.parsers.expat.ParserCreate()

		self.Parser.CharacterDataHandler = self.handleCharData
		self.Parser.StartElementHandler = self.handleStartElement
		self.Parser.EndElementHandler = self.handleEndElement

	def parse(self):
		self.Parser.Parse(self.xml_str)
	
	def handleCharData(self, data):
		pass

	def handleStartElement(self, name, attrs):
		if name == 'album':
			self.current_album = {}
			self.current_album['name'] = attrs['name']
			self.current_album['photos'] = []

		if name == 'photo':
			self.current_album['photos'].append({'path': attrs['path'], 'thumb': attrs['thumb']})


	def handleEndElement(self, name):
		if name == 'album':
			self.current_album['count'] = len(self.current_album['photos'])
			self.albums.append(self.current_album)


