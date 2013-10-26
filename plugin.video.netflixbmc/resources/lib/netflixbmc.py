import cookielib, urllib, urllib2
import re

class NetflixbmcScraper:
	def __init__(self):
		self.ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
		self.cj = cookielib.CookieJar()
   
	def GetAuthURL(self):
		url = 'https://signup.netflix.com/Login'
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		resp = opener.open(url)
		data = resp.read()
		match = re.search(r'.*?input.*?authURL.*?value.*?"(.*?)"', data)
		authURL = None
		if(match):
			authURL = match.group(1)
		return(authURL)

	def SignIn(self, email, password):
		url = 'https://signup.netflix.com/Login'
		authURL = self.GetAuthURL()
		headers = { 'User-Agent' : self.ua }
		post = urllib.urlencode({'email': email, 'password': password, 'authURL': authURL })
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		req = urllib2.Request(url, post, headers)
		opener.open(req)
		
	def GetMyList(self):
		url = 'http://movies.netflix.com/MyList?leid=595&link=seeall'
		hdrs = { 'User-Agent' : self.ua }
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		req = urllib2.Request(url, headers=hdrs)
		response = opener.open(req)
		data = response.read()
		
		results1 = re.search(r'.*?agMovieSet.*?agMovieGallery.*?list\-items">(.*)', data)
		pattern = re.compile(r'(<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?<\/div>)')

		titles = []
		for match in pattern.finditer(results1.group()): 
			title=match.group(2)
			boxart=match.group(3)
			movie = match.group(4)
			titles.append({'title': title, 'boxart': boxart, 'movie': movie})

		return(titles)

        def GetGenreList(self, id):
		page = 1
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		while True:
			url = 'http://movies.netflix.com/WiGenre?agid=%s&np=1&pn=%s' % (id, page)
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			req = urllib2.Request(url, headers=hdrs)
			response = opener.open(req)
			data = response.read()

			results1 = re.search(r'.*?agMovieSet.*?agMovieGallery">(.*)', data)
			if not results1:
				return(titles)

			pattern = re.compile(r'(<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?<\/div>)')

			matches = 0
			for match in pattern.finditer(results1.group()):
				title=match.group(2)
				boxart=match.group(3)
				movie = match.group(4)
				titles.append({'title': title, 'boxart': boxart, 'movie': movie})
				matches = matches + 1

			if matches < 40:
				return(titles)

			page = page + 1

		return(titles)

        def GetNewReleaseList(self):
		page = 1
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		while True:
			url = 'http://movies.netflix.com/WiRecentAdditionsGallery?d=/newReleases/all/release_date&np=1&pn=%d' % (page)
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			req = urllib2.Request(url, headers=hdrs)
			response = opener.open(req)
			data = response.read()

			results1 = re.search(r'.*?agMovieSet.*?agMovieGallery">(.*)', data)
			if not results1:
				return(titles)

			pattern = re.compile(r'(<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?<\/div>)')

			matches = 0
			for match in pattern.finditer(results1.group()):
				title=match.group(2)
				boxart=match.group(3)
				movie = match.group(4)
				titles.append({'title': title, 'boxart': boxart, 'movie': movie})
				matches = matches + 1

			if matches < 40:
				return(titles)

			page = page + 1

		return(titles)

