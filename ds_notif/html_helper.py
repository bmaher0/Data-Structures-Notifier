from HTMLParser import HTMLParser
import urllib

#a constant to store the URL of the calendar webpage
calendar_url = "http://www.cs.rpi.edu/academics/courses/spring16/csci1200/calendar.php" 

# create a subclass of HTML Parser
class DSSiteParser(HTMLParser):
	#the links of all link data
	links = []
	#used to store data found in links
	in_link = False
	def handle_starttag(self, tag, attrs):
		if tag == "a":
			self.in_link = True
	def handle_endtag(self, tag):
		if tag == "a":
			self.in_link = False
	def handle_data(self, data):
		#if the data is in a link, append to the list
		if self.in_link:
			self.links.append(data)

	#opens a page and returns a list of all the link data in the page
	def get_page_links(self, url):
		self.links = []
		page_file = urllib.urlopen(url)
		for line in page_file:
			self.feed(line)
		return self.links

#returns the link data for all the links in the calendar page
def get_calendar_links():
	return DSSiteParser().get_page_links(calendar_url)

if __name__ == "__main__":
	print get_calendar_links()
