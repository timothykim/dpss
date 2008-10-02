#!/usr/bin/env python
import xml.parsers.expat


class AlbumXMLParser():
	""" XML Parser class. Generates dictionary of album data from a xml file """
	def __init__(self, xml_str):
		""" Provide the xml string """
		
		self.albums = []
		self.current_album = {}
		self.xml_str = xml_str
	
	def parse(self):
		""" parse the xml string to generate the array of album dictionaries """
		parser = xml.parsers.expat.ParserCreate()
		
		parser.CharacterDataHandler = self.handleCharData
		parser.StartElementHandler = self.handleStartElement
		parser.EndElementHandler = self.handleEndElement
		
		parser.Parse(self.xml_str)
	
	def handleCharData(self, data):
		""" parser helper """
		pass
	
	def handleStartElement(self, name, attrs):
		""" parser helper """
		if name == 'album':
			self.current_album = {}
			self.current_album['name'] = attrs['name']
			self.current_album['photos'] = []

		if name == 'photo':
			self.current_album['photos'].append({'path': attrs['path'], 'thumb': attrs['thumb']})
		
	
	def handleEndElement(self, name):
		""" parser helper """
		if name == 'album':
			self.current_album['count'] = len(self.current_album['photos'])
			self.albums.append(self.current_album)


