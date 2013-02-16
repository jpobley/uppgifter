from bs4 import BeautifulSoup
import re, urllib, urllib2, json, time, pickle, csv, itertools
'''
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

ufodatafile = open('UFOdata.txt', 'r')
output2 = open('TheXFile.txt.', 'wb')
for line in ufodatafile:
	try:
		try:
			year = re.findall('<td.*?<font\scolor=\"#000000\"\sface=\"Calibri\"\sstyle=\"FONT-SIZE:11pt\"><a.*?>\d*?/\d.*?/(.*?)\s.+</a></font></td>', line)
			output2.write(year[0])
			output2.write('\t')
		except:
			try:
				sighting = re.findall('<td.*?<font\scolor=\"#000000\"\sface=\"Calibri\"\sstyle=\"FONT-SIZE:11pt\">(.*?)</font></td>', line)
				output2.write(str(sighting[0]))
				output2.write('\t')
			except:
				output2.write('\n')
	except:
		continue

output2.close()
WeAreNotAlone = open('TheXFile.txt.', 'r')
output3 = open('IWantToBelieve.txt', 'wb')

for line in WeAreNotAlone:
	try:
		line = line.split('\t')
		state = line[2]
		city = line[1]
		date = line[0]
		output3.write(date+'\t'+city+'\t'+state)
		output3.write('\n')
	except:
		continue
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
#all = pickle.load(open('sightingsStCo.pkl', 'rU'))
#print all["IL"]#["Marion"]

'''
#read in a bunch of census data into a list of lists, census data is stored in a modified csv file
#each line corresponds to either a state or a county in the USA and contains (among other items) median income and % pop. in poverty for all ages
#original file was obtained from http://www.census.gov/did/www/saipe/data/statecounty/data/2010.html
census_lol1 = []
census_csv_file1 = 'est10ALL-edited.csv'
census_lol1 = list(csv.reader(open(census_csv_file1, 'rU')))

#read in somem more densus data into a second list of lists, census data is stored in a modified csv file
#each line corresponds to either a state or a county in the USA and contains (among other items) population for that county
#original file was obtained from http://www.census.gov/popest/data/counties/totals/2011/index.html
census_lol2 = []
census_csv_file2 = 'CO-EST2011-Alldata-edited.csv'
census_lol2 = list(csv.reader(open(census_csv_file2, 'rU')))

#compare the two list of lists and append the second one onto the first where the counties match
for i in range(len(census_lol1)):
    for j in range(len(census_lol2)):
        if census_lol1[i][4] != 'State FIPS' and census_lol2[j][3] != 'state':
            if int(census_lol1[i][4]) == int(census_lol2[j][3]) and int(census_lol1[i][5]) == int(census_lol2[j][4]):
                #census_lol1[i] = census_lol1[i].append(census_lol2[j][7]) #this does not work for me, attempt was to append just the population for that county which is [7]. want to move on so going to just add the whole stupid list whenever the counties match. i am a bad programmer and we can change this later and remove my really long comment yeah that'd probably be good to do i think...
                census_lol1[i] = census_lol1[i] + census_lol2[j]

#become a pickle farmer, because that's cool, and so that we don't have to complete the 3 previous steps each time we execute this program
save = open('census_combined.pkl', 'wb')
pickle.dump(census_lol1, save)
save.close()
'''
''''
#go get that pickled combined census list of lists created previously
census = pickle.load(open('census_combined.pkl', 'rU'))

#change the UFO counts into single items lists in order to append corresponding census data for each county
for v1 in all.values():
    v1.update((k,[v]) for k,v in v1.iteritems()) 

#a little string chopper function so that census data county names match those obtained in Step 2
def chopper(fullcounty, ending): 
    if fullcounty.endswith(ending):
        return fullcounty[:-len(ending)]
    return fullcounty

#execute chopper funciton on all counties
for item in census: 
    item[0] = chopper(item[0], ' Parish') #Louisiana why do you have to be different?
for item in census:
    item[0] = chopper(item[0], ' Borough') #Alaska why do you have to be different?
for item in census:
    #Virginia is also different but it doesn't matter here because each of its cities that are not in a county (yes they have cities that are not in a county) have the word 'county' after them in the census data so it works out...but still...Virginia why do you have to be different?
    item[0] = chopper(item[0], ' County') #remove the ' County' from all counties minus the weirdos above

#horribly imbedded for/if loop with the lone end goal of appending the combined list census data for each county onto the proper county in dictionary of dictionaries of lists, after the number of UFOs
for state in all:
    for county in all[state]:
        for i in range(len(census)):
            if census[i][1] == state and census[i][0] == county:
                all[state][county] += census[i]

# from our final dictionary of dictionaries of lists named all,
# these are the pertitent items for us to correlate:
#
# all[state][county][0] = total reported UFO sitings in county
# all[state][county][3] = median household income of county
# all[state][county][4] =  percent (all ages) in poverty in county               
# all[state][county][32] = population of county

# richest county in the US via wikipedia table
print '   --- Brevard County Florida --- '
print '   Reported UFO sightings: ' + str(all["FL"]["Brevard"][0]) 
print '   Median Household Income: ' + str(all["FL"]["Brevard"][3])
print '   Percent (all ages) in Poverty: ' + str(all["FL"]["Brevard"][4])                
print '   Population: ' + str(all["FL"]["Brevard"][32])

# poorest county in the US via wikipedia table
#print 'Buffalo County South Dakota: '
#print all["SD"]["Buffalo"][0]  
#print all["SD"]["Buffalo"][3]  
#print all["SD"]["Buffalo"][4]                  
#print all["SD"]["Buffalo"][32]  
#############################################################################################
### uh oh, Houston we have a problem = where's the data for Buffalo County South Dakota?
### well, it's in the Census counties (in both Census CSV files) but looks
### like most likely there were no UFO sightings for this county so it simply
### does not make it into the dictionary of dictionaries of lists named all
### Perhaps this error supports our alternative alternative hypothesis:
### digital divide = no UFO reportings via NUFORC.org for poorest counties
###
### as it's 4:54am so I'm going to take a nap maybe when I wake up I'll have a fix -Darren
#############################################################################################
'''
