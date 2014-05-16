import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
from HTMLParser import HTMLParser
import re

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

#
#parser
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

#

nl = {}

rtllink = "http://www.rtl.hr"

if mode is None:
	url = build_url({'mode': 'rtl', 'foldername': 'RTL sada', 'link':'/rtl-sada/'})
	li = xbmcgui.ListItem('RTL sada', iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)	
	xbmcplugin.endOfDirectory(addon_handle)
	
# RTL sada
elif mode[0] == 'rtl':
	foldername = args['foldername'][0]
	link = args['link'][0]
	
	rex = re.compile(link+'[\w-]+/$');
	parser = MyHTMLParser()
	parser.feed(urllib.urlopen(rtllink+link).read())
	
	for n in nl:
		url = build_url({'mode': 'rtl', 'foldername': n, 'link': nl[n]})
		li = xbmcgui.ListItem(n, iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		
	rex = re.compile(link+'(\d*)/.*/$');	
	parser.feed(urllib.urlopen(rtllink+link).read())
	for n in nl:
		url = build_url({'mode': 'rtlxml', 'foldername': n, 'link': nl[n]+"?xml=1"})
		li = xbmcgui.ListItem(n, iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'rtlxml':
	#xbmc.Player().play(item='http://cdn-video1.rtl-hrvatska.hr/repository/media/f/7/f753f537136fac34d5af9c6433f71e9b.mp4?ver=1')
	link = rtllink+args['link'][0]
	foldername = args['foldername'][0]
	#pat = '<video><!\[cdata\[(.*)\]\]></video>'
	pat = '<video><!\[CDATA\[(.*)\]\]></video>'
	xml = urllib.urlopen(link).read()
	matchObj = re.findall(pat, xml, re.I)
	
	#url = build_url({'mode': 'rtl', 'foldername': 'RTL sada', 'link':'/rtl-sada/'})
	li = xbmcgui.ListItem(matchObj[0] , iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=matchObj[0], listitem=li)	
	
	
	# if matchobj:
		# #xbmc.player().play(item=matchobj[0])		
		# url = matchobj[0]
		# li = xbmcgui.listitem(foldername + ' video', iconimage='defaultvideo.png')
		# xbmcplugin.adddirectoryitem(handle=addon_handle, url=url, listitem=li)
    
	xbmcplugin.endOfDirectory(addon_handle)

	
elif mode[0] == 'rtlxmlll':
    foldername = args['foldername'][0]
    url = 'http://cdn-video1.rtl-hrvatska.hr/repository/media/1/3/13a8cd11add7ded30186b82ae7a3362f.mp4'
    li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)