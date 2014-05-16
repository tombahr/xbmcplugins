from HTMLParser import HTMLParser
import urllib
import re

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		# Only parse the 'anchor' tag.
		if tag == "a":
			# Check the list of defined attributes.
			take = False
			title=""
			link =""
			for name, value in attrs:
				# If href is defined, print it.				
				if name == "href":
					if rex.match(value):
						take = True
						link = value
				elif name == "title" and take:
					title = value
			if take and not title == "":
				#print title, " : ", link
				nl[title]=link

nl={}
		
rex = re.compile('/rtl-sada/serije/sulejman/'+'[\d]+/.+/$');			
					
parser = MyHTMLParser()
parser.feed(urllib.urlopen("http://www.rtl.hr/rtl-sada/serije/sulejman").read())

print nl

for n in nl:
	print nl[n]