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
'''
# Load pickle file of sightings dictionary
all = pickle.load(open('sightingsStCo.pkl', 'rU'))

# Read in a bunch of census data into a list of lists, census data is stored in a modified csv file
# Each line corresponds to either a state or a county in the USA and contains (among other items) median income and % pop. in poverty for all ages
# Original file was obtained from http://www.census.gov/did/www/saipe/data/statecounty/data/2010.html
census_lol1 = []
census_csv_file1 = 'est10ALL-edited.csv'
census_lol1 = list(csv.reader(open(census_csv_file1, 'rU')))

# Read in some more densus data into a second list of lists, census data is stored in a modified csv file
# Each line corresponds to either a state or a county in the USA and contains (among other items) population for that county
# Original file was obtained from http://www.census.gov/popest/data/counties/totals/2011/index.html
census_lol2 = []
census_csv_file2 = 'CO-EST2011-Alldata-edited.csv'
census_lol2 = list(csv.reader(open(census_csv_file2, 'rU')))

# Compare the two list of lists and append the second one onto the first where the counties match
for i in range(len(census_lol1)):
    for j in range(len(census_lol2)):
        if census_lol1[i][4] != 'State FIPS' and census_lol2[j][3] != 'state':
            if int(census_lol1[i][4]) == int(census_lol2[j][3]) and int(census_lol1[i][5]) == int(census_lol2[j][4]):
                #census_lol1[i] = census_lol1[i].append(census_lol2[j][7]) #this does not work for me, attempt was to append just the population for that county which is [7]. want to move on so going to just add the whole stupid list whenever the counties match. i am a bad programmer and we can change this later and remove my really long comment yeah that'd probably be good to do i think...
                census_lol1[i] = census_lol1[i] + census_lol2[j]

# Pickle the combined census data so we don't have to complete the 3 previous steps each time we execute this program
save = open('census_combined.pkl', 'wb')
pickle.dump(census_lol1, save)
save.close()

# Go get that pickled combined census list of lists we created 
census = pickle.load(open('census_combined.pkl', 'rU'))

# Change UFO counts into single item lists so that we can append corresponding census data for each county
for v1 in all.values():
    v1.update((k,[v]) for k,v in v1.iteritems()) 

#A little string chopper function so that census data county names match those obtained in Step 2 (usually we need to remove ' County' from each one, with a few exceptions)
def chopper(fullcounty, ending): 
    if fullcounty.endswith(ending):
        return fullcounty[:-len(ending)]
    return fullcounty

# Execute chopper funciton on all counties
for item in census: 
    item[0] = chopper(item[0], ' Parish') #Louisiana why do you have to be different?
for item in census:
    item[0] = chopper(item[0], ' Borough') #Alaska why do you have to be different?
for item in census:
    #Virginia is also different but it doesn't matter here because each of its cities that are not in a county (yes they have cities that are not in a county) have the word 'county' after them in the census data so it works out...but still...Virginia why do you have to be different?
    item[0] = chopper(item[0], ' County') #remove the ' County' from all counties minus the weirdos above

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

# From our final dictionary of dictionaries of lists named allData,
# these are the pertitent items:
# allData[state][county][0] = total reported UFO sitings in county
# allData[state][county][3] = median household income of county
# allData[state][county][4] =  percent (all ages) in poverty in county               
# allData[state][county][32] = population of county

'''

allData = pickle.load(open('all_data.pkl', 'rU'))

'''
# Write the pertitent fields (State, County, UFO Sightings, Median Household Income, Percent In Poverty, Population) to a TSV file, includes header
with open('ufos_income_poverty_by_county.txt', "w") as myFile:
    csv.register_dialect("custom", delimiter="\t", skipinitialspace=True)
    writer = csv.writer(myFile, dialect="custom")
    writer.writerow(("State", "County", "UFO Sightings", "Median Household Income (USD)", "Percent In Poverty", "Population" )) #create a header
    for state in allData:
        for county in allData[state]:
          if len(allData[state][county]) == 61:
            ctup = (state, county, allData[state][county][0], allData[state][county][3], allData[state][county][4], allData[state][county][32])
            writer.writerow(ctup)
'''

# To run scipy's pearsonr() function you must include two arguements, each must be a 1-dimensional list and the two lists must be the same length

# Create the lists to use in Pearson R correlation calculuations
ufos = []
income = []
poverty = []
population = []

# Get rid of the commas that appear in some numbers 
for state in allData:
    for county in allData[state]:
        if len(allData[state][county]) == 61:
            allData[state][county][3] = allData[state][county][3].replace(",", "")
            allData[state][county][4] = allData[state][county][4].replace(",", "")
            allData[state][county][32] = allData[state][county][32].replace(",", "")     

# Populate the lists that we will pass to the pearsonr() function
for state in allData:
    for county in allData[state]:
        # for triple if statement below:
        # 1) make sure county has census values, so 61 items
        # 2) get rid of those with dot for sightings value
        # 3) remove outliers from UFO sightings field. There are only outliers on high end (above 5810); low end outlier cutoff is below -5263, which is impossible.
        if len(allData[state][county]) == 61 and allData[state][county][3] != '.' and allData[state][county][0] < 5993:
            ufos.append(allData[state][county][0])
            income.append(int(allData[state][county][3]))
            poverty.append(float(allData[state][county][4]))
            population.append(int(allData[state][county][32]))
    
# For UFO sightings in each county, calculate Pearson's R values (linear correlation) and associated p-values
# for Median Household Income, Percent All Ages in Poverty, and Population
ufos_income = pearsonr(ufos,income)
ufos_poverty = pearsonr(ufos,poverty)
ufos_population = pearsonr(ufos,population)

# Print the Pearson's R results
print ' '
print ' -------------------------------------------------------- '
print ' --------- UFO Sightings in the U.S. by county ---------- '
print ' -------------------------------------------------------- '
print ' ----- Correlations and P-Vaues (using Pearson R) ------- '
print ' -------------------------------------------------------- '
print ' ------------ Correlation Coefficient    P-Value -------- '
print ' -------------------------------------------------------- '
print ' Median Income:    %s       %s ' % (ufos_income)
print ' %% in Poverty:    %s      %s ' % (ufos_poverty)
print ' Population:       %s      %s ' % (ufos_population)
print ' -------------------------------------------------------- '
print ' '
