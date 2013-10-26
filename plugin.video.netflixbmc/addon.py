import cookielib, urllib, urllib2
import os, re, sys, time
import xbmc, xbmcgui, xbmcplugin
from xbmcaddon import Addon
from resources.lib.netflixbmc import NetflixbmcScraper

__plugin__ = "Netflixbmc"
__authors__ = "hirodotp"
__credits__ = "hirodotp"

__settings__ = Addon( id="plugin.video.netflixbmc" )

class Main:
	def __init__(self):
		self._path = sys.argv[0]
		self._handle = int(sys.argv[1])
		self._get_settings()
		print str(sys.argv)
		print str(os.path)
		param = sys.argv[2]
		if param:
			param = param[1:]
			movie = param.split('movie=').pop(1)
			movie = urllib2.unquote(movie)
			print "Playing movie " + movie
			os.system("/usr/bin/firefox '%s' &" % (movie))
			time.sleep(int(self.settings['delay']))
			os.system("/usr/bin/xdotool mousemove 500 500")
			time.sleep(1)
			os.system("/usr/bin/xdotool click 1")
			time.sleep(5)
			os.system("/usr/bin/xdotool key f")
			time.sleep(1)
			os.system("/usr/bin/xdotool mousemove 0 0")
		else:
			self.scraper = NetflixbmcScraper()
			self.scraper.SignIn(self.settings['email'], self.settings['password'])
			self.mylist = self.scraper.GetMyList()
			self.DisplayMyList()

	def DisplayMyList(self):
		for item in self.mylist:
			listitem = xbmcgui.ListItem(item['title'], iconImage=item['boxart'], thumbnailImage=item['boxart'])
			print "Adding item " + str(item)
			movie = urllib.urlencode({'movie': item['movie']})
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?%s" % (self._path, movie), listitem=listitem, isFolder=False) 
		xbmcplugin.endOfDirectory( handle=self._handle, succeeded=True, cacheToDisc=False )

	def _get_settings( self ):
		# get the users preference settings
		self.settings = {}
		self.settings["email"] = __settings__.getSetting( "email" )
		self.settings["password"] = __settings__.getSetting( "password" )
		self.settings["delay"] = __settings__.getSetting( "delay" )

if __name__ == "__main__":
	import resources.lib.netflixbmc as plugin
	Main()
