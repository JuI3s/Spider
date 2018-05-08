#Very simple single thread spider gathering all internal links
from bs4 import BeautifulSoup 
import urllib2 
import requests 
from urlparse import urljoin

class Spider:

	def __init__(self, base_url):
		self.base_url = base_url
		self.to_crawl = []
		self.crawled = []
		self.finish = False

		self.to_crawl.append(self.base_url)

	#get all links contained in a url
	def get_links(self, url): 
		links = []
		try:
			r = requests.get(url)
			data = r.text
			soup = BeautifulSoup(data, 'html.parser')

			for each in soup.find_all('a'):
				link = each.get('href')
				link = urljoin(url, link)
				if link not in self.crawled and link not in self.to_crawl:
					links.append(link)
		except:
			print("Connection broken")

		return links

	def visit(self):
		if len(self.to_crawl):
			url = self.to_crawl[0]

			if self.base_url in url:
				print("Visiting site: " + url)
				links = self.get_links(url)

				if len(links):
					for link in links: 
						self.to_crawl.append(link)
				self.crawled.append(url)
				self.to_crawl.remove(url)
			else:
				self.to_crawl.remove(url)
		else:
			print("All links craweled!")
			self.finish = True

	def crawl(self):
		while self.finish == False:
			self.visit()
