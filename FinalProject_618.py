#from bs4 import BeautifulSoup
import re, urllib, urllib2, json, time, pickle, csv, itertools, string, random
from scipy.stats.stats import pearsonr

#####################################
##        Step One - Malcolm       ##
#####################################

#statesfile = open('state-abbreviations.csv')
#output1 = open('UFOdata.txt', 'wb')
'''
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

#load abbreviations
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
geo = {}
everything = {}
funnyStuff = re.compile(r'[0-9/\-?,!@#$%&*()]')
startNum = re.compile(r'^\d')
path = "AllStates_20121204/{0}_Features_20121204.txt"
years = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13"]
for state in abbr:
  stateDict = {}
  counties = {}
  cities = {}
  print "Scanning " + state + "..."
  f = open(path.format(state))
  features = f.readlines()
  f.close()
  for line in sightings:
    if line[0].isdigit():
      line = line.split('\t')
      yr = line[0]
      cty = line[1]
      st = line[2]
      if not funnyStuff.search(cty) and yr in years:
        if st == state:
          cities[cty] = cities.get(cty, 0) + 1
          for feat in features:
            feat = feat.split('|')
            if cty == feat[1] and feat[2] == "Populated Place":
              county = feat[5]
              counties[county] = counties.get(county, 0) + cities[cty]
              if county not in stateDict:
                stateDict[county] = (float(feat[9]), float(feat[10]))
  everything[state] = counties
  geo[state] = stateDict
#save dictionary of states--counties--sightings
save = open('sightingsStCo.pkl', 'wb')
pickle.dump(everything, save)
save.close()

#save dictionary of states--counties--coordinates
save = open('geo.pkl', 'wb')
pickle.dump(geo, save)
save.close()
'''
#######################################
##        Step Three - Darren        ##
#######################################

# Load pickle file of sightings dictionary
all = pickle.load(open('sightingsStCo.pkl', 'rU'))


###### pickle save / load break point ######



'''
# Read in a bunch of census data into a list of lists, census data is stored in a modified csv file
# Each line corresponds to either a state or a county in the USA and contains (among other items) median income and % pop. in poverty for all ages
# Original file was obtained from http://www.census.gov/did/www/saipe/data/statecounty/data/2010.html
census_lol1 = []
census_csv_file1 = 'est10ALL-edited.csv'
census_lol1 = list(csv.reader(open(census_csv_file1, 'rU')))

#remove unwanted fields
for i in range(len(census_lol1)): 
    census_lol1[i] = census_lol1[i][0:6]	

print census_lol1[0]
print census_lol1[1]
print census_lol1[-1]

# Read in some more densus data into a second list of lists, census data is stored in a modified csv file
# Each line corresponds to either a state or a county in the USA and contains (among other items) population for that county
# Original file was obtained from http://www.census.gov/popest/data/counties/totals/2011/index.html
census_lol2 = []
census_csv_file2 = 'CO-EST2011-Alldata-edited.csv'
census_lol2 = list(csv.reader(open(census_csv_file2, 'rU')))

#append proper number of 0's to FIPS county so it can match GEO.id2 filed w/education census data file
for i in range(len(census_lol1)):
    if len(census_lol1[i][5]) == 1:
	census_lol1[i][5] = '00' + census_lol1[i][5]
    elif len(census_lol1[i][5]) == 2:
	census_lol1[i][5] = '0' + census_lol1[i][5]
    elif len(census_lol1[i][5]) == 0:
	print "problem: len(census_lol1[i][5] == 0"
    elif len(census_lol1[i][5]) > 3:
	print '----------------'
	print 'problem: len(census_lol1[i][5] > 3, it is this one: %s' % i
	print i

#append proper number of 0's to FIPS county so it can match GEO.id2 field w/education census data file
for i in range(len(census_lol2)):
    if len(census_lol2[i][4]) == 1:
	census_lol2[i][4] = '00' + census_lol2[i][4]
    elif len(census_lol2[i][4]) == 2:
	census_lol2[i][4] = '0' + census_lol2[i][4]
    elif len(census_lol2[i][4]) == 0:
	print "problem: len(census_lol2[i][4] == 0"
    elif len(census_lol2[i][4]) > 3:
	print 'problem: len(census_lol2[i][4] > 3, it is this one: %s' % i
	#print i

# Compare the two list of lists and append the second one onto the first where the counties match
census_lol1[0].append("Population")
for i in range(len(census_lol1)):
    for j in range(len(census_lol2)):
	if census_lol1[i][4] + census_lol1[i][5] == census_lol2[j][3] + census_lol2[j][4]:
	    census_lol1[i].append(census_lol2[j][7])
	
		
# Read education census file, specifically HC01_VC17,Number; EDUCATIONAL ATTAINMENT - Population 25 years and over - Percent high school graduate or higher, obtained from the 2000 Decennial data file downloaded from here: http://factfinder2.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=DEC_00_SF3_DP2&prodType=table
census_lol3 = []
census_csv_file3 = 'DEC_00_SF3_DP2_with_ann-edited.csv'
census_lol3 = list(csv.reader(open(census_csv_file3, 'rU')))

# Compare the two list of lists and append the second one onto the first where the counties match
census_lol1[0].append("Percent High School Graduate (Age 25 Over)")
for i in range(len(census_lol1)):
    for j in range(len(census_lol3)):
	if i != 0:
	    if census_lol1[i][4] + census_lol1[i][5] == census_lol3[j][0]:
		census_lol1[i].append(census_lol3[j][1])
#
#print census_lol1[0]
#print census_lol1[1]
#print census_lol1[-1]
#print '---------------------'

# Read broadband access JSON file http://www.broadbandmap.gov/broadbandmap/county-availability/jun2012/nation?format=json
broadbandDict = json.loads(open('nation_broadband.json', 'rU').read())

# Compare the two list of lists and append the second one onto the first where the counties match
census_lol1[0].append("Broadband Availability Greater Than 50%")
for i in range(len(census_lol1)):
    fips = census_lol1[i][4] + census_lol1[i][5]
    broadband = ''
    #print broadbandDict['Results'][0]['countyId']
    if i != 0:
	for j in enumerate(broadbandDict['Results']):
	    if fips == broadbandDict['Results'][j[0]]['countyId']:
		if broadbandDict['Results'][j[0]]['availabilityGt50PercentFlag'] == True:
		    broadband = 1
		elif broadbandDict['Results'][j[0]]['availabilityGt50PercentFlag'] == False:
		    broadband = 0
		census_lol1[i].append(broadband)


print census_lol1[0]
print census_lol1[1]
print census_lol1[-1]

# Pickle the combined census data so we don't have to complete the 3 previous steps each time we execute this program
save = open('census_combined.pkl', 'wb')
pickle.dump(census_lol1, save)
save.close()
'''

###### pickle save / load break point ######


'''
# Go get that pickled combined census list of lists we created 
census = pickle.load(open('census_combined.pkl', 'rU'))


# Change UFO counts into single item lists so that we can append corresponding census data for each county
for v1 in all.values():
    v1.update((k,[v]) for k,v in v1.iteritems()) 

#A little string chopper function so that census data county names match those obtained in Step 2 (usually we need to remove ' County' from each one, with a few exceptions)
def chopper(fullcounty, ending): 
    if fullcounty.endswith(ending):
        return fullcounty[:-len(ending)]
    else:
	return fullcounty

# Execute chopper funciton on all counties
for item in census: 
    if item[0].endswith(' Parish'):
	item[0] = chopper(item[0], ' Parish') #Louisiana why do you have to be different?
    if item[0].endswith(' Borough'):	
	item[0] = chopper(item[0], ' Borough') #Alaska why do you have to be different?
    if item[0].endswith(' County'):	
	item[0] = chopper(item[0], ' County')
#Virginia is also different but it doesn't matter here because each of its cities that are not in a county (yes they have cities that are not in a county) have the word 'county' after them in the census data so it works out...but still...Virginia why do you have to be different?

# Append census data onto state--counties--ufos dictionary of dictionaries of lists
for state in all:
  for county in all[state]:
    for i in range(len(census)):
      if census[i][1] == state and census[i][0] == county:
        all[state][county] += census[i]
for i in range(len(census)):
  if census[i][1] in all and census[i][0] not in all[census[i][1]]:
    all[census[i][1]][census[i][0]] = all[census[i][1]].get(census[i][0],[0] + census[i])



# Save the new dictionary of states--counties--coordinates with the census data added for each county
save = open('all_data.pkl', 'wb')
pickle.dump(all, save)
save.close()
'''

###### pickle save / load break point ######



census = pickle.load(open('census_combined.pkl', 'rU'))
#print census[2]

allData = pickle.load(open('all_data.pkl', 'rU'))
#print allData['IL']['Marion']



###### pickle save / load break point ######


# Get rid of the comma that appears in median household income
for state in allData:
    for county in allData[state]:
	if len(allData[state][county]) == 10:
	    allData[state][county][3] = allData[state][county][3].replace(",", "")
   

# Write the pertitent fields (State, County, UFO Sightings, Median Household Income, Percent In Poverty, Population, Percent High School Graduate (Age 25 older)) to a TSV file, includes header
with open('ufos_income_poverty_by_county2.txt', "w") as myFile:
    csv.register_dialect("custom", delimiter="\t", skipinitialspace=True)
    writer = csv.writer(myFile, dialect="custom")
		    #create a header
    writer.writerow(("State",
		    "County",
		    "State FIPS",
		    "County FIPS",
		    "UFO Sightings",
		    "Median Household Income (USD)",
		    "Percent In Poverty",
		    "Population",
		    "Percent High School Graduate (Age 25 older)",
		    "Broadband Availability Greater Than 50%"))
		    
    for state in allData:
        for county in allData[state]:
          if len(allData[state][county]) == 10:
	    #print 'itititititiititititi'
            ctup = (state,
		    county,
		    allData[state][county][5],
		    allData[state][county][6],
		    allData[state][county][0],
		    allData[state][county][3],
		    allData[state][county][4],
		    allData[state][county][7],
		    allData[state][county][8],
		    allData[state][county][9])
            writer.writerow(ctup)
	    
myFile.close()

# Take a look at the 200 counties that have 0 for broadband...high correlations with poverty/low income as you'd expect?
#for state in allData:
#    for county in allData[state]:
#	if len(allData[state][county]) == 10:
#	    if allData[state][county][9] == 0:
#	        print allData[state][county]


###### pickle save / load break point ######


# To run scipy's pearsonr() function you must include two arguements, each must be a 1-dimensional list and the two lists must be the same length

# Create the lists to use in Pearson R correlation calculuations
ufos = []
income = []
poverty = []
population = []
highschool = []
broadband = []

# Populate the lists that we will pass to the pearsonr() function
for state in allData:
    for county in allData[state]:
        # for triple if statement below:
        # 1) make sure county has census values, so 61 items
        # 2) get rid of those with dot for sightings value
        # 3) remove outliers from UFO sightings field. There are only outliers on high end (above 5810); low end outlier cutoff is below -5263, which is impossible.
        if len(allData[state][county]) == 10 and allData[state][county][3] != '.' and allData[state][county][0] < 5993:
            ufos.append(allData[state][county][0])
            income.append(int(allData[state][county][3]))
            poverty.append(float(allData[state][county][4]))
            population.append(int(allData[state][county][7]))
	    highschool.append(float(allData[state][county][8]))
	    broadband.append(int(allData[state][county][9]))
    
# For UFO sightings in each county, calculate Pearson's R values (linear correlation) and associated p-values
# for Median Household Income, Percent All Ages in Poverty, Population, High School
ufos_income = pearsonr(ufos,income)
ufos_poverty = pearsonr(ufos,poverty)
ufos_population = pearsonr(ufos,population)
ufos_highschool = pearsonr(ufos,highschool)
ufos_broadband = pearsonr(ufos,broadband)

# Print the Pearson's R results
print ' '
print ' -------------------------------------------------------- '
print ' --------- UFO Sightings in the U.S. by county ---------- '
print ' -------------------------------------------------------- '
print ' ----- Correlations and P-Vaues (using Pearson R) ------- '
print ' -------------------------------------------------------- '
print ' ------------ Correlation Coefficient    P-Value -------- '
print ' -------------------------------------------------------- '
print ' Median Income:    %s        %s ' % (ufos_income)
print ' %% in Poverty:    %s      %s ' % (ufos_poverty)
print ' Population:       %s       %s ' % (ufos_population)
print ' High School:      %s       %s ' % (ufos_highschool) 
print ' Broadband:        %s      %s ' % (ufos_broadband) 
print ' -------------------------------------------------------- '
print ' '

