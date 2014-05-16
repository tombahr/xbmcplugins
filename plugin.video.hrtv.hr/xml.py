import urllib
import re
#import xml.etree.ElementTree as ET

#tree = ET.parse(urllib.urlopen("http://www.rtl.hr/rtl-sada/serije/sulejman/49215/sulejman-velicanstveni-261/?xml=1").read())
#root = tree.getroot()

pat = '<video><!\[CDATA\[(.*)\]\]></video>'
xml = urllib.urlopen("http://www.rtl.hr/rtl-sada/serije/tajne/49033/tajne-135/?xml=1").read()

matchObj = re.findall( pat, xml, re.I)

print matchObj[0]

# if matchObj:
	# print matchObj.group()

