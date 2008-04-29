#!/usr/bin/python
# -*- coding: utf-8 -*-


from twisted.web import server, resource, static
from twisted.internet import reactor

import sys
import os
import utilities


class Error(resource.Resource):
	def render_GET(self, request):
		return "<html>Album Request</html>"
	



def main():
	#first load the config file
	c = utilities.ServerConfig()
	
	#get the xml
	xml = utilities.XMLGenerator(c).generate()
	f = open("./www/albums.xml", "w");
	f.write(xml);
	f.close();
	
	#create a sym link?
	try:
		os.remove("./www/original")
	except Exception, e:
		pass
	
	try:
		os.remove("./www/thumb")
	except Exception, e:
		pass
	
	os.symlink(c.libpath, "./www/original")
	os.symlink(c.thumbpath, "./www/thumb")
	
	#serve the xml and the files
	root = static.File("./www")
	root.putChild("xml", static.File("./www/albums.xml"))
	
	
	#let's add albums
	# for album in xmlgen.albums:
	# 	a = root.putChild(album['name'], Error())
	# 	for pic in album['pictures']:
		
	
	site = server.Site(root)
	reactor.listenTCP(8407, site)
	reactor.run()



if __name__ == "__main__":
	main()