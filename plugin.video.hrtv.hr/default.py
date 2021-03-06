import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import re

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)



nl = {}
rtllink = "http://www.rtl.hr"


if mode is None:
	url = build_url({'mode': 'rtl', 'foldername': 'RTL sada', 'link':'http://www.rtl.hr/rtl-sada'})
	li = xbmcgui.ListItem('RTL sada', iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)	
	
	url = build_url({'mode': 'htv', 'foldername': 'HTV na zahtjev', 'link':'http://www.hrt.hr/enz/dnevnik/', 'level':0})
	li = xbmcgui.ListItem('HTV na zahtjev', iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	
	url = build_url({'mode': 'hts'})
	li = xbmcgui.ListItem('Uzivo', iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)
	
# RTL sada
elif mode[0] == 'rtl':
	foldername = args['foldername'][0]
	link = args['link'][0]
	
	###1 folder
	#link = '/rtl-sada'
	pat = r'<a href="('+link+'/[^/]*)/" title="([^"]*)">.*</a>'
	doc = urllib.urlopen(link).read()
	nl = re.findall( pat, doc, re.I)
	
	nl = list(set(nl))
	nl.sort()
	#print matchobj
	for n in nl:
		url = build_url({'mode': 'rtl', 'foldername': n[1], 'link': n[0]})
		li = xbmcgui.ListItem(n[1], iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	
	#2 epizode
	pat = '<a href="('+link+'/[\d]*/(?:[^/]*/){0,1})" title="([^"]*)">'
	nl = re.findall( pat, doc, re.I)
	nl.sort()
	for n in nl:
		url = build_url({'mode': 'rtlepizoda', 'foldername': n[1], 'link': n[0]})
		li = xbmcgui.ListItem(n[1], iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'rtlepizoda':
	#xbmc.Player().play(item='http://cdn-video1.rtl-hrvatska.hr/repository/media/f/7/f753f537136fac34d5af9c6433f71e9b.mp4?ver=1')
	link = args['link'][0]
	foldername = args['foldername'][0]
	#pat = '<video><!\[cdata\[(.*)\]\]></video>'
	pat = '{ "file": "([^"]*)"'
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

	
#HTV enz
elif mode[0] == 'htv':
	level = int(args['level'][0])	
	foldername = args['foldername'][0]
	link = args['link'][0]
	pat = ''
	folder = True
	if level==0: #lista emsija
		linkemisije = '//www.hrt.hr/enz'
		pat = '<a href="('+linkemisije+'/[\w-]*)/"><span>(.*)</span></a>'		
	elif level==1: #lista epizoda
		pat = r'<option(?: selected="selected")? value="(\d*)">([^<]*)' #(.*)</li>'
	elif level ==2: #epizoda
		pat= '<video data-url="([^"]*)"'
	
	doc = urllib.urlopen(link).read()
	nl = re.findall( pat, doc, re.I)
	nl = list(set(nl))
	nl.sort()
	olink=link
	for n in nl:
		isFolder = True
		name = foldername
		if level==1:
			link=olink+n[0]			
			name=n[1]
		elif level==0:			
			link='http:'+n[0]+'/'
			name=n[1]
		else:
			link = n
			name = foldername
			isFolder=False
		url = build_url({'mode': 'htv', 'foldername': name, 'link': link, 'level':level+1})
		if level == 2:
			url = link
		li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=isFolder)
	
	xbmcplugin.endOfDirectory(addon_handle)
	
elif mode[0] == 'rtlxmlll':
    foldername = args['foldername'][0]
    url = 'http://cdn-video1.rtl-hrvatska.hr/repository/media/1/3/13a8cd11add7ded30186b82ae7a3362f.mp4'
    li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'hts':
	url = 'http://83.139.104.100/Content/HLS/Live/Channel(HTV1-lpdbr)/Stream(03)/index.m3u8'
	li = xbmcgui.ListItem('HTV1', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	url = 'http://83.139.104.101/Content/HLS/Live/Channel(HTV2-abrdt)/Stream(03)/index.m3u8'
	li = xbmcgui.ListItem('HTV2', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	url = 'http://83.139.104.101/Content/HLS/Live/Channel(HTV3-zzrte)/Stream(03)/index.m3u8'
	li = xbmcgui.ListItem('HTV3', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	url = 'http://83.139.104.101/Content/HLS/Live/Channel(HTV4-miles)/Stream(03)/index.m3u8'
	li = xbmcgui.ListItem('HTV4', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.endOfDirectory(addon_handle)
