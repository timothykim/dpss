#!/usr/bin/env python
# encoding: utf-8
"""
loadconfig.py

Created by Timothy Kim
"""
import os
import ConfigParser


class Config:
	def __init__(self, cfile = None):
		#TODO: error checking
		self.cfile = cfile or ".dpss_conf"
		config = ConfigParser.ConfigParser()
		config.read(self.cfile)
		self.libpath = os.path.expanduser(config.get("server", "libpath"))
		self.thumbpath = os.path.expanduser(config.get("server", "thumbpath"))
		self.listtype = config.get("server", "listtype")
		self.ips = [ip.strip() for ip in config.get("server", "iplist").split(",")]
	
	
	def isValidIP(self, ip):
		"""docstring for isValidIP"""
		if self.listtype == "black":
			if self.ips.count(ip):
				return False
			else:
				return True
		else:
			if self.ips.count(ip):
				return True
			else:
				return False
				


class XMLGenerator:
	"""docstring for XMLGenerator"""
	def __init__(self, config):
		#TODO: check for path's existance
		self.libpath   = config.libpath
		self.thumbpath = config.thumbpath

	def generate(self):
		"""docstring for generate"""

		albums = []

		#parse through the director to make the album list
		for root, dirs, files in os.walk(self.libpath):
			for f in files[:]:
				if not (f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".JPG") or f.endswith(".JPEG")): files.remove(f)
			if len(files) > 0:
				albums.append({"name": os.path.basename(root), "path": root, "thumbpath": root.replace(self.libpath, self.thumbpath, 1), "pictures": files, })

		#return xml string
		xml = []
		xml.append('<?xml version="1.0" encoding="UTF-8"?>\n')
		xml.append('<albums count="' + str(len(albums)) + '">\n')
		for album in albums:
			xml.append('\t<album name="' + album['name'] + '" count="' + str(len(album['pictures'])) + '">\n')
			for pic in album['pictures']:
				xml.append('\t\t<photo path="' + album['path'] + "/" + pic + '" thumb="' + album['thumbpath'] + "/" + pic + '" />\n')
			xml.append('\t</album>\n')
		xml.append('</albums>\n')

		return ''.join(xml)
