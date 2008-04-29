#!/usr/bin/env python

import wx

servers = ["localhost", "localhost2"]
albums = [["Album 1", "Album 2", "Album 3"], ["Album 1", "Album 2"]]


class ServerList(wx.ListCtrl):
	def __init__(self, parent, id):
		"""docstring for fname"""
		wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
		self.parent = parent
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
		self.DeleteAllItems()
		for i in range(2):
			self.InsertStringItem(0, servers[i])
		
	
	
	def OnSelect(self, event):
		window = self.parent.GetGrandParent().FindWindowByName('AlbumList')
		index = event.GetIndex()
		window.LoadAlubums(index)
	


class AlbumList(wx.ListCtrl):
	"""docstring for AlbumList"""
	def __init__(self, parent, id):
		wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
		self.parent = parent
		self.LoadAlubums(0, '')
		
	def LoadData(self, index):
		self.DeleteAllItems()
		for album in albums[index]:
			self.InsertStringItem(0, album)
	

class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		"""docstring for __init__"""
		wx.Frame.__init__(self, parent, id, title)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
		
		vbox1 = wx.BoxSizer(wx.VERTICAL)
		panel1 = wx.Panel(splitter, -1)
		panel11 = wx.Panel(panel1, -1, size=(-1, 40))
		panel11.SetBackgroundColour('#53728c')
		st1 = wx.StaticText(panel11, -1, 'Servers', (5, 5))
		st1.SetForegroundColour('WHITE')
		
		panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
		vbox = wx.BoxSizer(wx.VERTICAL)
		list1 = ServerList(panel12, -1)
		
		vbox.Add(list1, 1, wx.EXPAND)
		panel12.SetSizer(vbox)
		panel12.SetBackgroundColour('WHITE')
		
		vbox1.Add(panel11, 0, wx.EXPAND)
		vbox1.Add(panel12, 1, wx.EXPAND)
		
		panel1.SetSizer(vbox1)
		
		vbox2 = wx.BoxSizer(wx.VERTICAL)
		panel2 = wx.Panel(splitter, -1)
		panel21 = wx.Panel(panel2, -1, size=(-1, 40), style=wx.NO_BORDER)
		st2 = wx.StaticText(panel21, -1, 'Articles', (5, 5))
		st2.SetForegroundColour('WHITE')
		
		panel21.SetBackgroundColour('#53728c')
		panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)
		vbox3 = wx.BoxSizer(wx.VERTICAL)
		
		list2 = AlbumList(panel22, -1)
		list2.SetName('AlbumList')
		vbox3.Add(list2, 1, wx.EXPAND)
		panel22.SetSizer(vbox3)
		
		
		panel22.SetBackgroundColour('WHITE')
		vbox2.Add(panel21, 0, wx.EXPAND)
		vbox2.Add(panel22, 1, wx.EXPAND)
		
		panel2.SetSizer(vbox2)
		
				
		self.Bind(wx.EVT_TOOL, self.ExitApp, id=1)
		
		hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
		self.SetSizer(hbox)
		splitter.SplitVertically(panel1, panel2)
		self.Centre()
		self.Show(True)
	
	def ExitApp(self, event):
		self.Close()
	
	



app = wx.App()
MainWindow(None, -1, 'F-Number')
app.MainLoop()

