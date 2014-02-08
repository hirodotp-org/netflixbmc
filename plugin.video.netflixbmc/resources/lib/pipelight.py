#!/usr/bin/env python

# Test for example with:
# python pipelight-xbmc.py "http://www.lovefilm.de/film/?token=%3Fu%3D%252Fcatalog%252Ftitle%252F326573%26m%3DGET"

# Modified by hirodotp to work with netflixbmc

import sys
import os
import tempfile
import shutil
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork

MOZILLA_PLUGINDIR = "/usr/lib/mozilla/plugins"
PIPELIGHT_LIBDIR  = "/usr/lib/pipelight"
PIPELIGHT_LIBRARY = "libpipelight.so"

class PipelightMainWindow(QtGui.QMainWindow):
	def __init__(self, page, cookies = []):
		QtGui.QMainWindow.__init__(self)
		self.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(0, 0, 0).name())

		self.cookies = cookies

		self.container = X11Container()
		self.setCentralWidget(self.container)

		os.putenv("PIPELIGHT_X11WINDOW", str(self.container.winId()))

		self.is_embedded 	= False
		self.browser 		= None
		self.browser_page   = page

		self.loadBrowser()
		#timer = QtCore.QTimer()
		#timer.singleShot(100, self.loadBrowser)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

	def loadBrowser(self):
		self.browser 		= Browser(self.browser_page, self.cookies)

		timer = QtCore.QTimer()
		timer.singleShot(10000, self.checkIfEmbedded)

	def checkIfEmbedded(self):
		if not self.is_embedded:
			print "Timeout reached and no Silverlight application embedded yet!"
			self.close()
			sys.exit(1)

	def close(self):
		os.unsetenv("PIPELIGHT_X11WINDOW")

		# Set to empty string to let Silverlight unload the page properly
		if self.browser is not None:
			self.browser.setHtml(QtCore.QString(""))
			self.browser = None

			timer = QtCore.QTimer()
			timer.singleShot(100, self.close)
			return

		QtGui.QMainWindow.close(self)

class X11Container(QtGui.QX11EmbedContainer):
	def __init__(self):
		QtGui.QX11EmbedContainer.__init__(self)
		QtCore.QObject.connect(self, QtCore.SIGNAL('clientIsEmbedded()'), self.clientIsEmbedded)
		QtCore.QObject.connect(self, QtCore.SIGNAL('clientClose()'), self.clientClose)

	def keyPressEvent(self, event):
		self.window().keyPressEvent(event)

	def clientIsEmbedded(self):
		self.window().is_embedded = True

	def clientClose(self):
		self.window().close()

class WebPage(QtWebKit.QWebPage):
	def userAgentForUrl(self, url):
		return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1"

class Browser(QtWebKit.QWebView):
	def __init__(self, url, cookies = []):
		QtWebKit.QWebView.__init__(self)
		self.resize(800,600)

		# setup cookies
		cookieList = []
		for cookie in cookies:
			cookieList.append(QtNetwork.QNetworkCookie(cookie[0], cookie[1]))
		cookieJar = QtNetwork.QNetworkCookieJar()
		cookieJar.setCookiesFromUrl(cookieList, QtCore.QUrl(url))
		nmanager = QtNetwork.QNetworkAccessManager()
		nmanager.setCookieJar(cookieJar)

		# create webpage
		page = WebPage()
		page.setNetworkAccessManager(nmanager)
		self.setPage(page)

		self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
		self.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
		QtCore.QObject.connect(self, QtCore.SIGNAL('loadFinished(bool)'), self.loadFinished)
		self.load(QtCore.QUrl(url))

	def loadFinished(self, ok):
		pass


class Pipelight:
	def __init__(self, pipelightName, pipelightDirectory, mozillaDirectory):
		self.pipelightName = pipelightName
		self.pipelightDirectory = pipelightDirectory
		self.mozillaDirectory = mozillaDirectory

		if not os.path.exists("%s/%s" % (self.pipelightDirectory, self.pipelightName)):
			print "It looks like pipelight is not installed! Unable to find '%s'." % self.pipelightName
			sys.exit(1)

		self.enabled_systemwide = os.path.exists("%s/%s" % (self.mozillaDirectory, self.pipelightName))
		self.plugin_tempdir = None

	def play(self, page, cookies = []):
		try:
			# Pipelight not enabled systemwide, create a temporary plugin dir
			if not self.enabled_systemwide:
				plugin_tempdir = tempfile.mkdtemp()
				os.symlink("%s/%s" % (self.pipelightDirectory, self.pipelightName), "%s/%s" % (plugin_tempdir, self.pipelightName))
				os.putenv("MOZ_PLUGIN_PATH", plugin_tempdir)

			# Show the Silverlight plugin in a QtGui window
			app = QtGui.QApplication([]) #(sys.argv) ?
			app.setAttribute(QtCore.Qt.AA_NativeWindows, True)
			mainWindow = PipelightMainWindow(page, cookies)
			mainWindow.showFullScreen()
			app.exec_()
		finally:
			# Delete the temporary plugin dir
			if plugin_tempdir is not None:
				try:
					shutil.rmtree(plugin_tempdir)
				except OSError as e:
					if e.errno != 2:
						raise

if __name__ == "__main__":
	print sys.argv
	sys.argv.pop(0)
	pipelightName = sys.argv.pop(0)
	pipelightDirectory = sys.argv.pop(0)
	mozillaDirectory = sys.argv.pop(0)
	gpuAccel = sys.argv.pop(0)
	url = sys.argv.pop(0)

	# force gpu acceleration if specified to
	if gpuAccel == "true":
		os.putenv("PIPELIGHT_GPUACCELERATION", "1")

	cookies = []
	c = []
	i = True
	for cookie in sys.argv:
		c.append(cookie)
		if i:
			i = False
		else:
			i = True
			cookies.append(c)
			c = []
			
	player = Pipelight(pipelightName, pipelightDirectory, mozillaDirectory)
	player.play(url, cookies)

