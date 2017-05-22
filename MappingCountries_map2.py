import requests
import pandas as pd
import json
import folium
mymap = folium.Map(location=[0,0],zoom_start=2)

countries = None
country_json = None
unique_locations = None
def initializeData():
	global countries
	countriesdf =pd.read_csv("/home/administrator/countries_for_mapping.csv",sep="\t")
        countries = countriesdf['numbers']
	countries.index=countriesdf['top_countries']

def getLocations():
	global country_json,unique_locations
	tempdiction = {}

	with open("country_members.json") as f:
		line = f.readline()
		line = "["+line.replace("\\n","").replace("\\","").replace(" ","").split("[")[1].rsplit("]")[0]+"]"
		country_json = json.loads(line)
	# print country_json
	for diction in country_json:
		key = diction["location"]
		latitude = diction["latitude"]
		longitude = diction["longitude"]
		tempdiction[key] = {"latitude":latitude,"longitude":longitude}
	country_json = tempdiction.copy()

	for old_key in country_json.copy():
		if len(old_key.split(",")) > 1:
			new_key = old_key.split(",")[1]
		else:
			new_key = old_key
		country_json[new_key] = country_json.pop(old_key)
	


def get_location(locationstring):

	locationstring = locationstring.replace(" ","")
	if locationstring in country_json:
		return country_json[locationstring]
	else:
		return {"latitude":None,"longitude":None}

def run():
	global mymap,unique_locations,country_json
	for loc in countries.index:
		coordinates = get_location(loc)
		lat = coordinates["latitude"]
		lon = coordinates["longitude"]
		count =  countries[loc]
		popup = "Location: {0}, Number of members {1}".format(loc,count)
		count = int(count)
		size = count*15
		if lat != None:
			mymap.circle_marker(location = [lat,lon],radius=size,fill_color="#3186cc",popup=popup, line_color='#3186cc')
	
	mymap.create_map(path="members_per_location.html")






initializeData()
getLocations()
run()
