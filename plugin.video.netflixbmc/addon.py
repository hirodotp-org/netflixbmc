import cookielib, urllib, urllib2
import subprocess
import os, re, sys, time
import xbmc, xbmcgui, xbmcplugin
from xbmcaddon import Addon
from PyQt4 import QtCore, QtGui
from resources.lib.netflixbmc import NetflixbmcScraper

__plugin__ = "Netflixbmc"
__authors__ = "hirodotp"
__credits__ = "hirodotp"

__settings__ = Addon( id="plugin.video.netflixbmc" )

TOP_CATEGORIES = [
			{'title': "Instant Queue", 'link': 'instant'}, 
			{'title': "New Release", 'link': 'new'},
			{'title': "Movies by Genre", 'link': 'genre'}
]

CAT_GENRES = [ 
		{'title': "Action & Adventure", 'link': 'action'}, 
		{'title': "Anime", 'link': 'anime'}, 
		{'title': "Children", 'link': 'children'}, 
		{'title': "Classics", 'link': 'classics'}, 
		{'title': "Comedies", 'link': 'comedies'}, 
		{'title': "Cult Movies", 'link': 'cult'}, 
		{'title': "Documentaries", 'link': 'documentaries'},
		{'title': "Dramas", 'link': 'dramas'},
		{'title': "Faith and Spirituality", 'link': 'faith'},
		{'title': "Foreign", 'link': 'foreign'},
		{'title': "Gay & Lesbian", 'link': 'gay'},
		{'title': "Halloween Favorites", 'link': 'halloween'},
		{'title': "Horror", 'link': 'horror'},
		{'title': "Independent", 'link': 'independent'},
		{'title': "Music", 'link': 'music'},
		{'title': "Musicals", 'link': 'musicals'},
		{'title': "Romance", 'link': 'romance'},
		{'title': "Science Fiction & Fantasy", 'link': 'scifi'},
		{'title': "Sports Movies", 'link': 'sports'},
		{'title': "Thrillers", 'link': 'thrillers'},
		{'title': "TV Shows", 'link': 'tv'}
]

GENRE_ID_MAP = {
			'action': '1365',
			'anime': '7424',
			'children': '783',
			'classics': '31574',
			'comedies': '6548',
			'cult': '7627',
			'documentaries': '6839',
			'dramas': '5763',
			'faith': '26835',
			'foreign': '7462',
			'gay': '5977',
			'halloween': '78429',
			'horror': '8711',
			'independent': '7077',
			'music': '1701',
			'musicals': '13335',
			'romance': '8883',
			'scifi': '1492',
			'sports': '4307',
			'thrillers': '8933',
			'tv': '83'
}

class Main:
	def __init__(self):
		self._path = sys.argv[0]
		self._handle = int(sys.argv[1])
		self._get_settings()

		param = sys.argv[2]
		if param:
			param = param[1:]
			try:
				movie = param.split('movie=').pop(1)
			except:
				movie = None

			try:
				category = param.split('category=').pop(1)
			except:
				category = None

			print "Movie " + str(movie)
			print "Category " + str(category)

			if movie:
				movie = urllib2.unquote(movie)
				print "Playing movie " + movie
				scraper = NetflixbmcScraper()
				scraper.SignIn(self.settings['email'], self.settings['password'])
				cookies = scraper.GetCookies()

				home = os.getenv("HOME")
				cmd = os.path.abspath("%s/.xbmc/addons/plugin.video.netflixbmc/resources/lib/pipelight.py" % (home))
				args = [cmd, movie]
				for cookie in cookies:
					args.append(cookie[0])
					args.append(cookie[1])

				print "Running ", args
				subprocess.call(args)

				#os.system("/usr/bin/firefox '%s' &" % (movie))
				#time.sleep(int(self.settings['delay']))
				#os.system("/usr/bin/xdotool mousemove 500 500")
				#time.sleep(1)
				#os.system("/usr/bin/xdotool click 1")
				#time.sleep(5)
				#os.system("/usr/bin/xdotool key f")
				#time.sleep(1)
				#os.system("/usr/bin/xdotool mousemove 0 0")
			elif category:
				category = urllib2.unquote(category)
				try:
					genre = category.split("//").pop(1)
					if genre:
						category = category.split("//").pop(0)
				except:
					genre = None
					

				print "Movie 2 " + str(genre)
				print "Category 2 " + str(category)
				

				if category == 'instant':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetMyList()
					self.DisplayMyList(mylist)
				elif category == 'new':
					scraper = NetflixbmcScraper()
					scraper.SignIn(self.settings['email'], self.settings['password'])
					mylist = scraper.GetNewReleaseList()
					self.DisplayMyList(mylist)
				elif category == 'genre':
					print "IN Category Genre"
					try:
						genre = genre.split("//").pop(0)
					except:
						genre = None

					print "genre: " + str(genre)

					if genre is None:
						self.DisplayGenres()
					else:
						scraper = NetflixbmcScraper()
						scraper.SignIn(self.settings['email'], self.settings['password'])
						mylist = scraper.GetGenreList(GENRE_ID_MAP[genre])
						self.DisplayMyList(mylist)
		else:
			self.DisplayTopCategories()

	def DisplayMyList(self, mylist):
		for item in mylist:
			listitem = xbmcgui.ListItem(item['title'], iconImage=item['boxart'], thumbnailImage=item['boxart'])
			print "Adding item " + str(item)
			movie = urllib.urlencode({'movie': item['movie']})
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?%s" % (self._path, movie), listitem=listitem, isFolder=False) 
		xbmcplugin.endOfDirectory(handle=self._handle, succeeded=True, cacheToDisc=False)

	def DisplayTopCategories(self):
		for item in TOP_CATEGORIES:
			listitem = xbmcgui.ListItem(item['title'])
			print "Adding item " + str(item)
			lnk = item['link']
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?category=%s" % (self._path, lnk), listitem=listitem, isFolder=True) 
		xbmcplugin.endOfDirectory( handle=self._handle, succeeded=True, cacheToDisc=False )
			
	def DisplayGenres(self):
		for item in CAT_GENRES: 
			listitem = xbmcgui.ListItem(item['title'])
			print "Adding item " + str(item)
			lnk = item['link']
			xbmcplugin.addDirectoryItem(handle=self._handle, url="%s?category=genre//%s" % (self._path, lnk), listitem=listitem, isFolder=True) 
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
