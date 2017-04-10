#Import the necessary library
import csv #to open data and write
import os #for dirctory information

import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import scipy.integrate as integrate
import scipy.special as special

#----------------------------------------------------------------------
#def analyze data
#Given the dictionary formatted data for each spot or county
#this function will build wave quality curves and do polyfitting
#-----------------------------------------------------------------------

def anaylzedata(datadict,spot_or_county, writer):
	
	for key in datadict: #iterate through the data structure

		#-----------------------------------------------------------------------
		#Access the data structures, printing to the console to track
		#-----------------------------------------------------------------------
		datapoints = datadict[key]	
		spot = key
		if(spot_or_county == "spot"):
			print "SPOT IS"
		else :
			print "COUNTY IS"

		print spot
		print "Points are"
		print datapoints

		if(len(datapoints) >= 3): # Maintains the rule of 3 condition
			xvar = [item[0] for item in datapoints] #separate out your variables here, for analytical purposes
			yvar = [item[1] for item in datapoints]
			
			#-----------------------------------------------------------------------
			#Now, you can do the fun stuff with the x/y variables.
			#First you get the polynomial fit and the correlation coefficient
			#-----------------------------------------------------------------------
			
			try:
				z = np.polyfit(xvar, yvar, 5) #the number here is the degree of the polynomial function
				f = np.poly1d(z)
			except:
				print "Few data points, polyfit may be fragile"

			print "The polyfit fucntion is:"
			print f  #this is the polynomial function

			try:
				coeff = np.corrcoef(xvar, yvar) #generates the correlation coefficient
			except:
				print "Few data points, correlation coefficient may be fragile"

			print "The correlation coefficient is:"
			print coeff[0][1] #because of the library formatting, this is how to access the integer value

			#-----------------------------------------------------------------------
			#This is the specific formatting for the graphs on plotly
			#-----------------------------------------------------------------------
			xnew = np.linspace(xvar[0], xvar[-1], 50)
			ynew = f(xnew) 

			trace1 = go.Scatter(
				x = xvar,
				y = yvar,
				mode = "markers",
				name = "Responses"
			)

			trace2 = go.Scatter(
				x = xnew,
				y = ynew,
				mode = "lines",
				name = "Line Of Best Fit"
			)

			data = [trace1, trace2]

			xlabels = ["","Low","Medium","High","Very High"]
			ylabels = ["","Very Poor","Okay","Fair","Good","Best"]
			xaxis = go.XAxis(
				title = "Tide Level",
				#range = [1,4],
				ticks = "",
				showticklabels = True,
				ticktext = xlabels,
				#zeroline = False,
				tickvals = [i for i in range(len(xlabels))]
			)

			yaxis = go.YAxis(
				title = "Wave Quality",
				ticks = "",
				showticklabels = True,
				ticktext = ylabels,
				tickvals = [i for i in range(len(ylabels))]
			)

			layout = go.Layout(title = key,
						       yaxis = yaxis,
			                   xaxis = xaxis
			         )


			#-----------------------------------------------------------------------
			#Now you can send the chart info to plotly and see/save the charts
			#-----------------------------------------------------------------------
			
			#fig = go.Figure(data = data, layout = layout) #sends info to plotly
			#py.plot(fig, filename=spot)
			#py.image.save_as(fig, filename="Batch 2/"+spot + ".png") #Creates a local file of the image

			#-----------------------------------------------------------------------
			#Now calculate the wave quality integrals, now and in the future
			#-----------------------------------------------------------------------

			#want the integral of f from 1 to 3 = current wave quality
			currentquality = integrate.quad(f, 1, 3) # returns a tuple of the result and the estimate of error
			#want the inegral of f from 2 to 4 = future wave quality
			futurequality = integrate.quad(f, 2, 4)
			difference = futurequality[0] - currentquality[0]

			print ("The current quality is ", currentquality[0])
			print ("The future quality is ", futurequality[0])
			print ("The difference is " ,difference)
			print ("Which normalized is ", (difference/currentquality[0]*100), "percent")
			
			#Generate a csv with all this info formatted in an efficient way
			writer.writerow([(spot),(datapoints),(f),(coeff[0][1]),(currentquality[0]),(futurequality[0]),(difference),(difference/currentquality[0]*100)])


#----------------------------------------------------------------------
#Boilerplate, opening the file, creating an iterator on it
#------------------------------------------------------------------------
fileopener = open("clean-master.csv","rb")
datareader = csv.reader(fileopener, delimiter = ",")

writername = "Batch 2/Wave Quality Results.csv"
writefileopener = open(writername,"wb")
writer = csv.writer(writefileopener)

writer.writerow([("Surf Spot"),("Points"),("Polyfit Function"),("Correlation Coefficient"),("Current Quality Integral"),("Future Quality Integral"),("Absolute Difference"),("Percentage Difference")])
titlerow = datareader.next() #so we know which column is which

#-----------------------------------------------------------------------
#create the dictionary-formatted data structure to store wave quality
#responses to further analyze later one
#-----------------------------------------------------------------------

indexofsurfspot = titlerow.index("CSURFSPOT")
indexofbesttide = titlerow.index("BESTTIDE")  #very low = 1, very high = 7
indexofcounty = titlerow.index("SPOTCO")
indexofBTLow = titlerow.index("BESTTIDELOW")
indexofBTMed = titlerow.index("BESTTIDEMED")
indexofBTHigh = titlerow.index("BESTTIDEHIGH")
indexofBTVHigh = titlerow.index("BESTTIDEVHIGH")

#-----------------------------------------------------------------------
#Data structures that can be analyzed later on
#-----------------------------------------------------------------------
datadict = {}
for spot in places:
	datadict[spot] = []

countydict = {}
for county in counties:
	countydict[county] = []

#-----------------------------------------------------------------------
#All the places and counties, for aggregating purposes
#-----------------------------------------------------------------------
places = ["Huntington Beach","Bird Rock","Ocean Beach","Horseshoes","RCA","26th Avenue",
		"Dunes at Spanish Bay","El Porto","Scripps","Malibu","Princeton Jetty","Seals",
		"Fort Point","Blacks","Pipes","Seal Beach Southside","Turn Arounds","36th Street",
		"Hammonds","San Clemente State Beach","San Onofre","Ocean Beach SD Pier",
		"Huntington Beach Pier Southside","Salmon Creek","Topanga","Silver Strand",
		"56th Street","Cardiff","Pacifica","Pleasure Point","Scott Creek","PB Point",
		"Mission Beach","Garbage","County Line","Huntington Beach Pier","D Street",
		"C Street","Pacific Beach","Uppers","Trestles","The Pit","Campgrounds",
		"Ray Bay","Leo Carillo","Oceanside Pier","Moss Landing","Sunset","Church",
		"Rockaway","Huntington Beach Goldenwest (aka Dog Beach, Cliffs)","Mission Beach Jetty",
		"Cowells","Sunset Cliffs","Brown House","Deveroux","0","Ocean Beach South",
		"Scripps Pier","Getchells","Torrey Pines","North Jetty","Abalones","Swamis",
		"Rincon","Salt Creek","Davenport","La Jolla Shores","Dockweiller State Beach",
		"Strands","Steamer Lane","Hazard Canyon","54th Street","Secos",
		"Huntington Beach Sunset Beach","Mavericks","Zuma","San Onofre - The Point",
		"Hanimonds","Patrick's Point","Seaside","The Rock","Pismo Beach Pier","Ponto",
		"Big Rock","Santa Clara Rivermouth","Huntington Beach Pier Northside","Del Mar",
		"Bolinas Patch","Laguna Creek","Marine Street","Little Rincon","Bolsa Chica Tower 20",
		"The Hook","Deadmans","Manresa","Pillbox","Bolinas","Rock Slides","4 Mile","Beacons",
		"Westhaven","Morro Strand","Pacifica Pier","Cherry Hill","Reef Rights","38th Avenue",
		"Cayucos Beach","The Wedge","Capitola Jetty","Asilomar","Santa Ana River Jetties",
		"Leadbetter","Point Dume","Carmel","Grandview","Boneyards","Salt Point","Big River",
		"Swift","Huntington Beach Smokestacks","15th Street","Studios","Venice Beach Breakwater",
		"Ventura Harbor","Manhattan Beach","Bird Rock South Bird","Rockpile","Trails","Oceanside",
		"Seal Beach Pier","Half Moon Bay","Sharks Cove","Avocados","Harimos","Avalanche",
		"Newport Point","Thalia","Tourmaline","Pismo Beach Pier Northside","Cottons","Oceano Dunes",
		"The River","Oceanside Harbor","Newport Beach West","xSecret Spotx","Waddell","Old Mans",
		"Blackies","Tabletops","PB Drive","Ocean Beach SD","Manhattan Beach Pier","Bolsa Chica",
		"Chasms","Fort Cronkite","Sands","Pitas Point","3 Mile","Needles","Middles","Naples",
		"Hermosa Beach","South Moss at Spanish Bay","Terra Mar","Newport Beach","Calafia",
		"Windansea","Staircase Beach","Tower 37","PB Cove","The Hole","Dog Patch","Bay Street",
		"La Conchita","Torrance Beach","Refugio","San Clemente Clocktower","Solimar","Natural Bridges",
		"Moss Landing Jetty","Emma Wood","Campus Point","Powerhouse","Wisconsin Street","Ocean Park",
		"Zeros","New Brighton Beach","Ross's Cove","La Piedra","Law Street","Buccaneer Beach",
		"Ventura Cove","Dillon Beach","Seascape","El Morro","Three Arch Bay","Imperial Beach Pier",
		"Lunada Bay","Tamarack","8/9th Street Del Mar","Ocean Beach SD Jetty","Marina Beach",
		"Hospitals","Seal Beach","Suckouts","Morro Bay","Imperial Beach","Sewers","Venice Beach Pier",
		"Jalama","Luscombs","Oceanside Pier Southside","Scripps Pier Northside","Privates",
		"Point Arena","Port Hueneme Pier","Coronado","San Clemente Lausens","Ralphs","Avila Beach",
		"Casas","Oceanside Jetty Northside","Pismo Beach","Cabrillo Point","Killers","Tioga","Montara",
		"In-Betweens","PV Cove","Santa Clause Lane","Burnout","Hollywood Beach","Rockview","Riviera",
		"Pacifica Boat Docks","Bolsa Chica Tower 21","Sewerline","Shelter Cove","Latigo Point",
		"Moonlight Beach","Tarantulas","Venice Beach","Del Monte","Japs","Labs","Hope Ranch"]

counties = ["Orange","San Diego","San Francisco","Marin","Santa Cruz",
			"Monterey","Los Angeles","San Mateo","Santa Barbara","Sonoma","Ventura",
			"San Luis Opisbo","Humboldt","Mendocino"]

#-----------------------------------------------------------------------
#Can loop through all rows and build up the dictionaries for analytical purposes
#-----------------------------------------------------------------------

for row in datareader: #iterate through each row of the data file
	spot = row[indexofsurfspot] #find the spot in that row
	county = row[indexofcounty] # and the county

	if(len(spot) == 0):  continue
	datapoints = datadict[spot] #get the array of responses already in the array for that spot
	countydata = countydict[county] #do the same for the county responses so far

	lowpoint = row[indexofBTLow] #collect all the data here
	medpoint = row[indexofBTMed]	
	highpoint = row[indexofBTHigh]
	vhighpoint = row[indexofBTVHigh]

	if(len(lowpoint) == 1 and len(medpoint) == 1 and len(highpoint) == 1 and len(vhighpoint) ==1 ): #excludes poins that dont have all responses
		datapoints.append([1,float(lowpoint)])
		datapoints.append([2,float(medpoint)])
		datapoints.append([3, float(highpoint)])		
		datapoints.append([4, float(vhighpoint)])

		countydata.append([1,float(lowpoint)])
		countydata.append([2,float(medpoint)])
		countydata.append([3, float(highpoint)])		
		countydata.append([4, float(vhighpoint)])

	datadict[spot] = datapoints #now put the array of responses back into the dictionary
	countydict[county] = countydata #do the same for county


#-----------------------------------------------------------------------
#Now you have the dictionaries built up, so you can analyze the data
#-----------------------------------------------------------------------
anaylzedata(datadict,"spot",writer)
writer.writerow([("County"),("Points"),("Polyfit Function"),("Correlation Coefficient"),("Current Quality Integral"),("Future Quality Integral"),("Absolute Difference"),("Percentage Difference")])
anaylzedata(countydict,"county",writer)

