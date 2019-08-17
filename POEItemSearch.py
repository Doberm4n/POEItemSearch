# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QUrl
import res.res
import sys
import os
import generated.main as GUIMain
import generated.about as GUIAbout
from Tkinter import Tk
import ctypes
import json
import lzstring
import webbrowser
import subprocess
# dummy imports for pyinstaller. See
# https://github.com/google/rekall/issues/303
if 0:
	import UserList
	import UserString
	import UserDict
	import itertools
	import collections
	import future.backports.misc
	import commands
	import base64
	import __buildin__
	import math
	import reprlib
	import functools
	import re
	

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

form = None
formAbout = None
version = '0.9.1'
linkHTML = '<a href="https://github.com/Doberm4n/POEItemSearch">https://github.com/Doberm4n/POEItemSearch</a>'
link = 'https://github.com/Doberm4n/POEItemSearch'


class POEItemSearchApp(QtGui.QMainWindow, GUIMain.Ui_MainWindow):

	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.pasteButton.clicked.connect(self.pasteFromClipboard)
		self.actionAbout.triggered.connect(self.showAbout)
		self.config = self.loadConfig()
		self.browserPath = self.config['settings']['browserPath'].encode("utf-8")
		self.leagueName = self.config['settings']['leagueName']


	def pasteFromClipboard(self):
			temp = Tk()
		try:
			self.dataTextEdit.setPlainText('')
			clipboardData = temp.selection_get(selection = "CLIPBOARD").splitlines()
			if not 'Rarity' in clipboardData[0]: return
			itemName = clipboardData[1]
			data = {
				"attributes.league": self.leagueName,
				"info.tokenized.fullName": itemName
			};
			self.dataTextEdit.setPlainText(itemName)	
			lz_string = lzstring.LZString()
			data = lz_string.compressToBase64(unicode(json.dumps(data)))
			subprocess.Popen(self.browserPath + " https://poeapp.com/#/search/" + data, shell=True)
		except:
			pass
		

	def loadConfig(self):
		try:
			with open('config\\config.json') as data_file:
				return json.load(data_file)
		except Exception, e:
			return


	def showAbout(self):
		global formAbout
		formAbout = aboutDialog()
		formAbout.show()


class aboutDialog(QtGui.QDialog, GUIAbout.Ui_Dialog):
	def __init__(self):
		global version
		global linkHTML
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.WindowTitleHint)
		self.linkLabel.linkActivated.connect(self.openURL)
		self.versionLabel.setText("v." + version)
		self.linkLabel.setText(linkHTML)
		pic = self.picLabel
		pic.setPixmap(QtGui.QPixmap(":search-icon32.png"))


	def openURL(self, linkStr):
		global link
		webbrowser.open(link)


def main():
	app = QtGui.QApplication(sys.argv)
	appIco = QtGui.QIcon()
	appIco.addFile(':search.png', QtCore.QSize(256,256))
	app.setWindowIcon(appIco)
	form = POEItemSearchApp()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()
