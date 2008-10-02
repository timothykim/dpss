#!/usr/bin/env python
# encoding: utf-8
"""
Utility Module

Configuration Parsing and XML generator

Created by Timothy Kim
"""
import os
import ConfigParser
import re


class ClientConfig:
	""" Client Config file parser Class """
	def __init__(self, cfile = None):
		""" Constructor, opnes the specified configuration file. Default = "dpss_client.conf" """
		#TODO: error checking
		self.cfile = cfile or "dpss_client.conf"
		config = ConfigParser.ConfigParser()
		config.read(self.cfile)
		self.buddylist = filter(self.filterIP, [ip.strip() for ip in config.get("client", "buddylist").split(",")]);
	
	def filterIP(self, ip):
		""" Filters out the bad IPs """
		for n in ip.split("."):
			unit = int(n)
			if unit < 0 or unit > 255:
				return None
		return ip
	
	def isValidIP(self, ip):
		""" Validates IP address """
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


class ServerConfig:
	""" Server Config file parser Class """
	
	def __init__(self, cfile = None):
		""" Constructor, opnes the specified configuration file. Default = "dpss_server.conf" """
		self.cfile = cfile or "dpss_server.conf"
		config = ConfigParser.ConfigParser()
		config.read(self.cfile)
		self.libpath = os.path.expanduser(config.get("server", "libpath"))
		self.thumbpath = os.path.expanduser(config.get("server", "thumbpath"))
		self.listtype = config.get("server", "listtype")
		self.ips = filter(self.filterIP, [ip.strip() for ip in config.get("server", "iplist").split(",")]);
	
	def filterIP(self, ip):
		""" Filters out the bad IPs """
		for n in ip.split("."):
			unit = int(n)
			if unit < 0 or unit > 255:
				return None
		return ip
	
	def isValidIP(self, ip):
		""" Validates IP address """
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
	"""XML Generator Class"""
	def __init__(self, config):
		""" configuration files are read in """
		#TODO: check for path's existance
		self.libpath   = config.libpath
		self.thumbpath = config.thumbpath

	def generate(self):
		""" Scans the directory specified the configuration and generates the xml file """
		
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
				xml.append('\t\t<photo path="' + album['path'].replace(self.libpath, '', 1) + "/" + pic + '" thumb="' + album['thumbpath'].replace(self.thumbpath, '', 1) + "/" + pic + '" />\n')
			xml.append('\t</album>\n')
		xml.append('</albums>\n')
		
		return ''.join(xml)
	


