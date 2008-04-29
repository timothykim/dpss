#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncore, socket
from xmlparser import AlbumXMLParser

class XMLGetter(asyncore.dispatcher):
    def __init__(self, host, path):
        self.xml_buffer = []
        self.xml = ""
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 8407) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.xml = ''.join(self.xml_buffer)
        a,b,self.xml = self.xml.partition("\r\n\r\n")
        self.close()

    def handle_read(self):
        self.xml_buffer.append(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]



