from bs4 import BeautifulSoup
import re, urllib, urllib2, json, time, pickle

#####################################
##        Step One - Malcolm       ##
#####################################
'''
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
'''
#################################
##        Step Two - JP        ##
#################################
'''
#read txt file from step one
f = open('IWantToBelieve.txt', 'rU')
sightings = f.readlines()
f.close()

abbr = statesfile.readlines()
statesfile.close()

#strip \n character from each line in abbr
i = 0
while i < len(abbr):
    abbr[i] = abbr[i].rstrip('\r\n')
    i += 1
    
#strip \n character from each line in citystate
i = 0
while i < len(sightings):
    sightings[i] = sightings[i].rstrip('\r\n')
    i += 1

#read cities and counties and sightings per county into massive dictionary
everything = {}
funnyStuff = re.compile(r'[0-9/\-?,!@#$%&*()]')
path = "AllStates_20121204/{0}_Features_20121204.txt"
for state in abbr:
  counties = {}
  cities = {}
  print "Scanning " + state + "..."
  f = open(path.format(state))
  features = f.readlines()
  f.close()
  for line in sightings:
    if not funnyStuff.search(line):
      city, st = line.split('\t')
      if st == state:
        cities[city] = cities.get(city, 0) + 1
        for feat in features:
          feat = feat.split('|')
          if city == feat[1] and feat[2] == "Populated Place":
            county = feat[5]
            counties[county] = counties.get(county, 0) + cities[city]
  everything[state] = counties
save = open('sightingsStCo.pkl', 'wb')
pickle.dump(everything, save)
save.close()
'''
#######################################
##        Step Three - Darren        ##
#######################################

#load pickle file of sightings dictionary
all = pickle.load(open('sightingsStCo.pkl', 'rU'))
print all["MI"]["Washtenaw"]
