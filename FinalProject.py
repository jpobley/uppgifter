from bs4 import BeautifulSoup
import re, urllib2, json, time

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
