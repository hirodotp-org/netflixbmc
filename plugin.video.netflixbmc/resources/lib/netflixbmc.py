import cookielib, urllib, urllib2
import re
import random

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
		
	def GetCookies(self):
		cookies = []
		for cookie in self.cj:
			cookies.append([cookie.name, cookie.value])
		return cookies

	def GetMyList(self):
		url = 'http://movies.netflix.com/MyList'
		hdrs = { 'User-Agent' : self.ua }
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		req = urllib2.Request(url, headers=hdrs)
		response = opener.open(req)
		data = response.read()
		titles = []
		
		# check if we are using manual sorting or not
		res = re.search(r'Change order to:.*?MANUAL.*?</a>', data)
		if not res:
			# using manual sorting
			res = re.search(r'<input class="evoSubmit" type="submit" value="Update List">(.*)', data, re.DOTALL)
			data = res.group(1)
			pattern = re.compile(r'<span class="title.*?"><a.*?>(.*?)</a></span>.*?<td.*?href=\'(.*?)\'', re.DOTALL)
			for match in pattern.finditer(data):
				title = match.group(1)
				movie = match.group(2)
	
				# generate boxart url
				# The Virgin Suicides","boxshots":{"small":3960650,"medium":3960652,"large":3960654}}
				boxart = ''
				searchStr = r'","boxshots":{"small":.*?,"medium":.*?,"large":(.*?)}}'
				searchStr = "%s%s" % (title, searchStr)
				res = re.search(searchStr, data)
				if res:
					boxid = res.group(1)
					boxgroup = boxid[-4:]
					cdn = random.randrange(0, 9)
					boxart = "http://cdn%d.nflximg.net/images/%s/%s.jpg" % (cdn, boxgroup, boxid)
				
				# append movie to title list
				titles.append({'title': title, 'boxart': boxart, 'movie': movie})
		else:
			# using auto sorting
			results1 = re.search(r'.*?agMovieSet.*?agMovieGallery.*?list\-items">(.*)', data)
			pattern = re.compile(r'(<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?<\/div>)')

			if results1:
				for match in pattern.finditer(results1.group()): 
					title=match.group(2)
					boxart=match.group(3)
					movie = match.group(4)
					# append movie to title list
					titles.append({'title': title, 'boxart': boxart, 'movie': movie})

		return(titles)

        def GetGenreList(self, id, maxResults, kids = False):
		page = 1
		total = 0
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		while True:
			if kids:
				url = 'http://www.netflix.com/KidsAltGenre?agid=%s&np=1&pn=%s' % (id, page)
			else:
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

			total = total + matches
			page = page + 1

			if matches < 40 or total >= maxResults:
				break

		return(titles)

        def GetNewReleaseList(self):
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		url = 'http://movies.netflix.com/NewReleases'
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		req = urllib2.Request(url, headers=hdrs)
		response = opener.open(req)
		data = response.read()

		pattern = re.compile(r'<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?</div>', re.DOTALL)

		for match in pattern.finditer(data):
			title=match.group(1)
			boxart=match.group(2)
			movie = match.group(3)
			titles.append({'title': title, 'boxart': boxart, 'movie': movie})

		return(titles)

	def GetRecentReleaseList(self):
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		url = 'http://movies.netflix.com/WiRecentAdditionsGallery?nRR=arrivalDate&nRT=all'
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		req = urllib2.Request(url, headers=hdrs)
		response = opener.open(req)
		data = response.read()

		pattern = re.compile(r'<div class="agMovie.*?boxShotImg.*?alt="(.*?)".*?src="(.*?)".*?href="(.*?)".*?</div>', re.DOTALL)

		for match in pattern.finditer(data):
			title=match.group(1)
			boxart=match.group(2)
			movie = match.group(3)
			titles.append({'title': title, 'boxart': boxart, 'movie': movie})

		return(titles)

	def GetHDReleaseList(self, maxResults):
		page = 1
		total = 0
		titles = []
		hdrs = { 'User-Agent' : self.ua }

		while True:
			url = 'http://movies.netflix.com/WiHD?np=1&pn=%s' % (page)
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

			total = total + matches
			page = page + 1

			if matches < 40 or total >= maxResults:
				break

		return(titles)
