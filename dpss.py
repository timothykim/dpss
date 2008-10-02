#!/usr/bin/env python
"""
	DPSP Module
	
	GUI Front End
"""

import wx
import client
from os.path import basename

#event ID constants
ID_SEVER_TREE = 001

ID_CONNECT_IP = 101
ID_ADD_IP = 102
ID_IMPORT = 103
ID_IMPORT_ALL = 104
ID_QUIT = 105

ID_SELECT_ALL = 111
ID_REFRESH = 112
ID_PREF = 113


class MainWindow(wx.Frame):
	""" Main Window Class. Nothing fancy here. """
	def __init__(self, parent, id, title, client):
		"""
			Constructor
			
			Populates the left tree pane.
		"""
		wx.Frame.__init__(self, parent, id, title, size=(800,500))
		
		self.client = client
		
		
		#create the main pain
#		self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)		
		splitter = wx.SplitterWindow(self, -1)
		
		#create the server list panel
		
		self.tree = wx.TreeCtrl(splitter, ID_SEVER_TREE, wx.DefaultPosition, (-1, -1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
		root = self.tree.AddRoot('Connections')
		
		servers = []
		for server in self.client.servers:
			albums = self.client.getAlbums(server)
			if albums:
				s = self.tree.AppendItem(root, server + " (" + str(len(albums)) + ")")
				for album in albums:
					a = self.tree.AppendItem(s, album['name'] + " (" + str(album['count']) + ")")
					#self.tree.SetPyData(a, album['photos'])
					for photo in album['photos']:
						p = self.tree.AppendItem(a, basename(photo['path']))
						photo["server"] = server
						self.tree.SetPyData(p, photo)
				servers.append(s)
			
		
		self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelection, id=ID_SEVER_TREE)
		
		
		#picture viewer
		# self.picture_panel = wx.Panel(splitter, -1)
		# self.picture_box = wx.GridSizer(20,3,5,5)
		# self.picture_panel.SetSizer(self.picture_box)
		
		self.picture_panel = wx.Panel(splitter, -1)
		self.picture = wx.StaticBitmap(self.picture_panel)
		
		
		splitter.SplitVertically(self.tree, self.picture_panel)
		
		
		
		#create status bar
		self.statusbar = self.CreateStatusBar()
		
		#create tool bar 
		toolbar = self.CreateToolBar(wx.NO_BORDER | wx.TB_HORIZONTAL, -1, "Tool Bar")
		toolbar.AddSimpleTool(ID_CONNECT_IP, wx.Image('images/connect.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Connect', '')
		toolbar.AddSimpleTool(ID_REFRESH, wx.Image('images/refresh.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Refresh', '')
		toolbar.AddSeparator()
		toolbar.AddSimpleTool(ID_QUIT, wx.Image('images/exit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Quit', '')
		toolbar.Realize()
		
		self.Bind(wx.EVT_TOOL, self.OnConnect, id = ID_CONNECT_IP)
		self.Bind(wx.EVT_TOOL, self.OnRefresh, id = ID_REFRESH)
		self.Bind(wx.EVT_TOOL, self.OnQuit, id = ID_QUIT)
		
		#menu system
		filemenu = wx.Menu()
		filemenu.Append(ID_CONNECT_IP, "&Connect to IP", " Connect to a remote computer")
		filemenu.Append(ID_ADD_IP, "&Add IP", " Add an IP")
		filemenu.AppendSeparator()
		filemenu.Append(ID_IMPORT, "&Import Selected", " Import selected pictures")
		filemenu.Append(ID_IMPORT_ALL, "&Import All", " Import All Pictures from selected album")
		filemenu.AppendSeparator()
		filemenu.Append(ID_QUIT, "Q&uit", " Terminate the program")
		
		editmenu = wx.Menu()
		editmenu.Append(ID_SELECT_ALL, "&Select All", " Select all pictures")
		editmenu.Append(ID_REFRESH, "&Refresh", " Refresh Server List")
		editmenu.Append(ID_PREF, "&Preferences"," Change the settings")
		
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(editmenu, "&Edit")
		self.SetMenuBar(menuBar)
		self.Centre()
		self.Show(True)
	
	def OnConnect(self, event):
		""" Connect to a user specified server and update the GUI """
		
		self.statusbar.SetStatusText('Connecting...')
		dialog = wx.TextEntryDialog(self, 'Please Enter an IP to connect to:', 'Connect to IP')
		dialog.SetValue("127.0.0.1")
		#if dialog.ShowModal == wx.ID_OK:
			#self.client.connect(dialog.GetValue())
		dialog.Destroy()
	
	def OnRefresh(self, event):
		""" Reconnect to all the servers """
		self.statusbar.SetStatusText('Refreshing...')
		
	
	def OnTreeSelection(self, event):
		""" Event handler for tree item selections """
		item = event.GetItem()
		photo = self.tree.GetPyData(item)
		if photo:
			p = self.client.getThumb(photo["server"], photo["thumb"])
			self.picture.SetBitmap(wx.Bitmap(p))
			self.Refresh()
	
	def OnQuit(self, event):
		""" Event handler for quiting """
		self.Close()

def main():
	c = client.Client()

	app = wx.App(0)
	MainWindow(None, -1, 'DPSS', c)
	app.MainLoop()


if __name__ == "__main__":
	main()