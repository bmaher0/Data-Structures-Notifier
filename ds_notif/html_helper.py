from HTMLParser import HTMLParser
import urllib

calendar_url = "http://www.cs.rpi.edu/academics/courses/spring16/csci1200/calendar.php" 

# create a subclass and override the handler methods
class DSSiteParser(HTMLParser):
	links = []
	in_link = False
	def handle_starttag(self, tag, attrs):
		if tag == "a":
			self.in_link = True
	def handle_endtag(self, tag):
		if tag == "a":
			self.in_link = False
	def handle_data(self, data):
		if self.in_link:
			self.links.append(data)
	def get_page_links(self, url):
		page_file = urllib.urlopen(url)
		for line in page_file:
			self.feed(line)
		return self.links

def get_calendar_links():
	return DSSiteParser().get_page_links(calendar_url)

if __name__ == "__main__":
	print get_calendar_links()
