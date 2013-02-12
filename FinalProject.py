from bs4 import BeautifulSoup
import re, urllib, urllib2, json, time, pickle

#####################################
##        Step One - Malcolm       ##
#####################################

#statesfile = open('state-abbreviations.csv')
#output1 = open('UFOdata.txt', 'wb')

#for line in statesfile:
#	state = line.strip()
#	print state
#	print 'working...'
#	ufosite = urllib2.urlopen('http://www.nuforc.org/webreports/ndxl'+state+'.html')
#	ufosoup = BeautifulSoup(ufosite)
#	x = ufosoup.tbody.find_all('tr')
#	print 'writing...'
#	output1.write(str(x))
#	print 'sleeping...'
#	time.sleep(5)
#output1.close()

#ufodatafile = open('UFOdata.txt', 'r')
#output2 = open('TheXFile.txt.', 'wb')
#for line in ufodatafile:
#	try:
#		sighting = re.findall('<td.*?<font\scolor=\"#000000\"\sface=\"Calibri\"\sstyle=\"FONT-SIZE:11pt\">(.*?)</font></td>', line)
#		try:
#			output2.write(str(sighting[0]))
#			output2.write('\t')
#		except:
#			output2.write('\n')
#	except:
#		continue

#output2.close()
#WeAreNotAlone = open('TheXFile.txt.', 'r')
#output3 = open('IWantToBelieve.txt', 'wb')

#for line in WeAreNotAlone:
#	try:
#		line = line.split('\t')
#		state = line[2]
#		city = line[1]
#		output3.write(city+'\t'+state)
#		output3.write('\n')
#	except:
#		continue

#################################
##        Step Two - JP        ##
#################################

#read txt file from step one
f = open('IWantToBelieve.txt', 'rU')
citystate = f.readlines()
f.close()
f = open("text.txt", "wb")

#strip \n character from each line
i = 0
while i < len(citystate):
    citystate[i] = citystate[i].rstrip('\n')
    i += 1

cities = {}
regex = re.compile(r'[(),0-9/-?.@#$]')
for line in citystate:
  real = "AL"
  city, state = line.split('\t')
  if state == real:
    if not regex.search(city):
      cities[city] = cities.get(city, 0) + 1
print cities
#half = "_Features_20121204.txt"

'''
address = 'Wyoming (various towns)	WY'
county = ''
base_url = 'http://maps.googleapis.com/maps/api/geocode/xml?'
data = {}
data['address'] = address
data['sensor'] = 'false'
full_url = base_url + urllib.urlencode(data)
response = urllib2.urlopen(full_url)
info = response.read()
root = ET.fromstring(info)
for each in root.findall('.//address_component'):
  if each.find('type') is not None:
    if each.find('type').text == "administrative_area_level_2":
      zipcode = each.find('long_name').text
'''