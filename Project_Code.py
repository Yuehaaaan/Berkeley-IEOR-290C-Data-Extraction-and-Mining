"""
url = http://www.kiva.org/teams?queryString=&category=all&membershipType=all&startDate=&endDate=&userId=&sortBy=overallLoanedAmount&pageID=1

"""

import json
import requests
from bs4 import BeautifulSoup
import csv
import gc
import resource

class KivaTeam:
	def __init__(self):
		self.url = None
		self.about = {"about":{"team_url":None,"team_name":None,"date_founded":None,"intro":None,"about_us":None,"team_members":None,
					   		    "amount_loaned":None,"loans":None,"loans_per_member":None, "category":None}}
		self.loans = {"loans":{}}
		self.members = {"members":{}}		
		self.impact = {"impact":{"borrower_female_percentage":None,"borrower_female_count":None,
								 "borrower_male_percentage":None,"borrower_male_count":None,
								 "total_amount_lent":None,
								 "total_loans":None,"loans_this_month":None,
								 "loans_per_member":None,"team_members":None,
								 "new_members_this_month":None,"countries":None,
								}
						}
		self.topCountries = {"top_countries":{}}
		self.topSectors = {"top_sectors":{}}
	def getURL(self):
		return self.url
	def getAbout(self):
		return self.about
	def getLoans(self):
		return self.loans
	def getMembers(self):
		return self.members
	def getImpact(self):
		return self.impact
	def getTopCountries(self):
		return self.topCountries
	def gettopSectors(self):
		return self.topSectors

		
	def emptyInAbout(self):
		result = ""
		for key,value in self.about["about"].items():
			if value == None:
				result = result + "{0} in ABOUT is empty. URL:{1}\n".format(key,self.url)
		result = result.rstrip("\n")
		return result
		
	def emptyInLoans(self):
		if not self.loans["loans"]:
			return "LOANS is empty. URL:{0}".format(self.url)
		return ""

	
	def emptyInMembers(self):
		if not self.members["members"]:
			return "MEMBERS is empty. URL:{0}".format(self.url)
		return ""

		
	def emptyInImpact(self):
		result = ""
		for key,value in self.impact["impact"].items():
			if value == None:
				result = result + "{0} in IMPACT is empty. URL:{1}\n".format(key,self.url)
		result = result.rstrip("\n")
		return result

	def emptyInTopCountries(self):
		if not self.topCountries["top_countries"]:
			return "TOP COUNTRIES is empty. URL:{0}".format(self.url)
		return ""

	def emptyInTopSectors(self):
		if not self.topSectors["top_sectors"]:
			return "TOP SECTORS is empty. URL:{0}".format(self.url)
		return ""


def getJson(url):
	response = requests.get(url)
	sc = response.status_code
	if sc != 200:
		print "Error getting URL: %s" %sc
		return -1
	jsonValue = json.loads(response.content)
	return jsonValue
		
def getSoup(url):
	"""Given a url, return parsed html of BeautifulSoup, return -1 if error"""
	response = requests.get(url)
	sc = response.status_code
	if sc != 200:
		print "Error getting URL: %s" %sc
		return -1
	content = response.content
	soup = BeautifulSoup(content)
	return soup

def getKivaPageLinks(page_num):
	"""Given a page number, return the Kiva Lending Teams links of that page, -1 if error"""
	base_url = "http://www.kiva.org/teams?queryString=&category=all&membershipType=all&startDate=&endDate=&userId=&sortBy=overallLoanedAmount&pageID={0}"
	links = []
	target_url = base_url.format(page_num)
	soup = getSoup(target_url)
	if soup == -1:
		soup
	table_ul = soup.find("ul",{"class":"teamCards listing stack"})
	table_article = table_ul.findAll("article")
	if len(table_article) == 0:
		print "{0} not found".format(page_num)
		return -1
	else:
		for article in table_article:
			link = article.find("a")["href"]
			links.append(link)
		return links

def setTeamURL(kivaTeam,url):
	kivaTeam.url = url

def setTeamAbout(kivaTeam):
	"""Takes in a KivaTeam and a url and update the About Section, return -1 if error"""
	base_url = "http://www.kiva.org/team/"
	url = kivaTeam.getURL()
	if base_url not in url:
		print "invalid url:{0}".format(url)
		return -1
	soup = getSoup(url)
	if soup == -1:
		return -1


	#!!!!! NEED TO CHECK FOR EMPTY LISTS!!!!!!!!!!!!!!!!!!!!!


	#set the team url
	kivaTeam.about["about"]["team_url"] = kivaTeam.url

	# search for the team category
	div = soup.find("div",{"class":"meta"})
	category = div.find("a").text.strip()
	kivaTeam.about["about"]["category"] = category

	#search for the team name
	kivaTeam.about["about"]["team_name"] = soup.find("h2",{"class":"hPage"}).text.split(":")[1].strip()

	#search for the founded date
	date_text = soup.find("div",{"class":"meta"}).text.split("since")[1].strip()
	day = date_text.split()[1].replace(",","").strip()
	year = date_text.split()[-1].strip()
	if "Jan" in date_text:
		month = "-01-"
	elif "Feb" in date_text:
		month = "-02-"
	elif "Mar" in date_text:
		month = "-03-"
	elif "Apr" in date_text:
		month = "-04-"
	elif "May" in date_text:
		month = "-05-"
	elif "Jun" in date_text:
		month = "-06-"
	elif "Jul" in date_text:
		month = "-07-"
	elif "Aug" in date_text:
		month = "-08-"
	elif "Sep" in date_text:
		month = "-09-"
	elif "Oct" in date_text:
		month = "-10-"
	elif "Nov" in date_text:
		month = "-11-"
	elif "Dec" in date_text:
		month = "-12-"

	kivaTeam.about["about"]["date_founded"] = year+month+day

	TeamAbout = soup.findAll("p",{"class":"big g6 a z"})

	#search for the introduction
	if len(TeamAbout) > 0:
		kivaTeam.about["about"]["intro"] = TeamAbout[0].text.replace("\n"," ").strip()

	#search for the about us
	if len(TeamAbout) > 1:
		kivaTeam.about["about"]["about_us"] = TeamAbout[1].text.replace("\n"," ").strip()

	
	TeamImpact = soup.findAll("div",{"class":"impactValue"})

	#search for the team members
	text = TeamImpact[0].text.replace(",","").strip()
	number = int(text)
	kivaTeam.about["about"]["team_members"] = number

	#search for the amount loaned
	text = TeamImpact[1].text.replace(",","").replace("$","").strip()
	number = int(text)
	kivaTeam.about["about"]["amount_loaned"] = number

	#search for loans
	text = TeamImpact[2].text.replace(",","").strip()
	number = int(text)
	kivaTeam.about["about"]["loans"] = number

	#search for loans per number
	text = TeamImpact[3].text.replace(",","").strip()
	number = float(text)
	kivaTeam.about["about"]["loans_per_member"] = number

	
	TeamRankings = soup.findAll("table",{"class":"rankings"})

	#search for rankings across all teams
	temp_diction = {"allranking_loaned_alltime":0,"allranking_loaned_thismonth":0,
						"allranking_loaned_lastmonth":0,"allranking_user_alltime":0,
						"allranking_user_thismonth":0,"allranking_user_lastmonth":0}
	if len(TeamRankings) > 1:
		ranking_td = TeamRankings[0].findAll("td")
		for td in ranking_td:
			key = td.text
			value = int(td.text.split("for")[0].replace("#","").strip())
			if "Amount Loaned (All Time)" in key:
				temp_diction["allranking_loaned_alltime"] = value
			elif "Amount Loaned (This Month)" in key:
				temp_diction["allranking_loaned_thismonth"] = value
			elif "Amount Loaned (Last Month)" in key:
				temp_diction["allranking_loaned_lastmonth"] = value
			elif "New Users (All Time)" in key:
				temp_diction["allranking_user_alltime"] = value
			elif "New Users (This Month)" in key:
				temp_diction["allranking_user_thismonth"] = value
			elif "New Users (Last Month)" in key:
				temp_diction["allranking_user_lastmonth"] = value
	kivaTeam.about["about"].update(temp_diction)


	#search for rankings in common interest category
	temp_diction = {"commonranking_loaned_alltime":0,"commonranking_loaned_thismonth":0,
						"commonranking_loaned_lastmonth":0,"commonranking_user_alltime":0,
						"commonranking_user_thismonth":0,"commonranking_user_lastmonth":0}
	if len(TeamRankings) > 2:
		ranking_td = TeamRankings[1].findAll("td")
		for td in ranking_td:
			temp_diction = {}
			key = td.text
			value = int(td.text.split("for")[0].replace("#","").strip())
			if "Amount Loaned (All Time)" in key:
				temp_diction["commonranking_loaned_alltime"] = value
			elif "Amount Loaned (This Month)" in key:
				temp_diction["commonranking_loaned_thismonth"] = value
			elif "Amount Loaned (Last Month)" in key:
				temp_diction["commonranking_loaned_lastmonth"] = value
			elif "New Users (All Time)" in key:
				temp_diction["commonranking_user_alltime"] = value
			elif "New Users (This Month)" in key:
				temp_diction["commonranking_user_thismonth"] = value
			elif "New Users (Last Month)" in key:
				temp_diction["commonranking_user_lastmonth"] = value
		kivaTeam.about["about"].update(temp_diction)

	return 1


def  getKivaPageLoanLink(team_url,page_num):
	"""Takes in a team url and the page number to go to, return a url to that page number"""
	
	base_url = "http://www.kiva.org/team/"
	if base_url not in team_url:
		print "Invalid team url: {0}".format(team_url)
		return -1
	target_url = team_url+"/loans?pageID={0}".format(page_num)
	soup = getSoup(target_url)
	if soup == -1:
		return soup

	return target_url

def setTeamLoans(kivaTeam):
	"""Given a KivaTeam and its url, update the loans section of the class, return -1 if error"""
	#! For some reason, the maximum page we can go to is 300 before it begins to display page 1 again
	team_url = kivaTeam.getURL()
	page_num = 0
	# page_num is set to 10 due to time constraint
	while (page_num < 10):

		loan_url = getKivaPageLoanLink(team_url,page_num)
		base_diction = {"name":None,"category":None,"country":None,
					"raising_status":None,"repayment_status":""}

		#!!!!! NEED TO CHECK FOR EMPTY LISTS!!!!!!!!!!!!!!!!!!!!!
		soup = getSoup(loan_url)
		if soup == -1:
			return soup

		loanTable = soup.find("ul",{"class":"loanCards default "})
		loanList = loanTable.findAll("li")
		
		for li in loanList:
			temp_diction = {}
			loan_id = int(li.find("article",{"class":"loanCard default vertical "})["id"].split("_")[-1])
			info_status = li.find("span",{"class":"info_status"})
			base_diction["name"] = info_status.find("div",{"class":"name"}).text.strip()
			base_diction["category"] = info_status.find("div",{"class":"activity"}).text.strip()
			base_diction["country"] = info_status.find("div",{"class":"country"}).text.strip()
			base_diction["raising_status"] = info_status.find("span",{"class":"status"}).text
			#Missing repaid percentage
			temp_diction[loan_id] = base_diction.copy()
			kivaTeam.loans["loans"].update(temp_diction)
		page_num = page_num + 1

	return 1


def getKivaPageMemberLink(team_url):

	"""Give a Kiva team url, return the json path to the members of the team, -1 if error"""
	
	# from the team_url get the team id
	members_url = team_url+"/members"
	soup =  getSoup(members_url)
	scripts = soup.findAll("script")
	for script in scripts:
		if "team_id" in script.text:
			mixed_text = "%s" %(script.text.split("{",1)[1].rsplit("}",1)[0])
			jsonValue = "{%s}" %(mixed_text.split("{",1)[1].split("}",1)[0].strip())
			value = json.loads(jsonValue)
			team_id  = value["team_id"]
	members_url = "https://api.kivaws.org/SirenV1/team/{0}/members".format(team_id)
	return members_url



def setTeamMembers(kivaTeam):
	"""Give a KivaTeam and its team url, update the members section of the class, return -1 if error"""
	team_url = kivaTeam.getURL()
	members_url = getKivaPageMemberLink(team_url)
	members_json = getJson(members_url)
	temp_diction = {}

	for entity in members_json["entities"]:
		temp = [entity][0].get("entities",None)
		if temp != None:
			name = temp[0]["properties"].get("name","")
			location = temp[0]["entities"][0]["properties"].get("whereabouts","")
			temp_diction[name] = location
	kivaTeam.members["members"].update(temp_diction.copy())

def getKivaPageImpactLink(team_url):
	"""Given a team url, return the impact page link, -1 if error"""
	base_url = "http://www.kiva.org/team/"
	if base_url not in team_url:
		print "Invalid team url: {0}".format(team_url)
		return -1
	target_url = team_url+"/impact"
	soup = getSoup(target_url)
	if soup == -1:
		return soup

	return target_url

def setTeamImpact(kivaTeam):
	"""Given a Kiva Team and its team url, set the impact section of the team, return -1 if error """
	team_url = kivaTeam.getURL()
	impact_url = getKivaPageImpactLink(team_url)
	soup = getSoup(impact_url)
	if soup == -1:
		return soup


	# search for gender related information
	all_gender_percentage = soup.findAll("span",{"class":"borrowerGenderPercentage"})
	all_gender_count = soup.findAll("span",{"class":"borrowerGenderCount"})

	female_percentage = float(all_gender_percentage[0].text.split("%")[0].strip())
	female_count = int(all_gender_count[0].text.strip().replace(",","")[1:-1])

	male_percentage = float(all_gender_percentage[1].text.split("%")[0].strip())
	male_count = int(all_gender_count[1].text.replace(",","").strip()[1:-1])

	kivaTeam.impact["impact"]["borrower_female_percentage"] = female_percentage
	kivaTeam.impact["impact"]["borrower_male_percentage"] = male_percentage
	kivaTeam.impact["impact"]["borrower_male_count"] = male_count
	kivaTeam.impact["impact"]["borrower_female_count"] = female_count

	# search for total amount lent
	total_amount_lent_text = soup.find("div",{"class":"totalLentLegendAmount"}).text
	total_amount_lent = float(total_amount_lent_text.replace("$","").replace(",","").strip())
	kivaTeam.impact["impact"]["total_amount_lent"] = total_amount_lent

	#search of top sectors (this is not sorted)
	team_sector_list = soup.find("ul",{"class":"teamSectorsList"})
	team_sector_li = team_sector_list.findAll("li",{"class":"teamSectorItem"})

	temp_diction = {}
	for li in team_sector_li:
		sector_name = li.find("div",{"class":"sectorName"}).text.strip()
		sector_num = int(li.find("div",{"class":"sectorStat"}).text.split()[0].replace(",","").strip())
		temp_diction[sector_name] = sector_num
	kivaTeam.topSectors["top_sectors"].update(temp_diction)

	# search for team stats
	stats_table = soup.find("ul",{"class":"teamStatsList"})
	stats_li = stats_table.findAll("li",{"class":"teamsStat"})
	for li in stats_li:
		category = li.find("div",{"class":"number_caption"}).text.strip()
		if category == "Total loans":
			text = li.find("div",{"class":"number_sans"}).text.replace(",","").strip()
			number = int(text)
			kivaTeam.impact["impact"]["total_loans"] = number
		elif category == "Loans this month":
			text = li.find("div",{"class":"number_sans"}).text.replace(",","").strip()
			number = int(text)
			kivaTeam.impact["impact"]["loans_this_month"] = number
		elif category == "Loans per member":
			text = li.find("div",{"class":"number_sans"}).text.replace(",","").strip()
			number = float(text)
			kivaTeam.impact["impact"]["loans_per_member"] = number
		elif category == "Team members":
			text = li.find("div",{"class":"number_sans"}).text.replace(",","").strip()
			number = int(text)
			kivaTeam.impact["impact"]["team_members"] = number
		elif category == "New members this month":
			text = li.find("div",{"class":"number_sans"}).text.replace(",","").strip()
			number = int(text)
			kivaTeam.impact["impact"]["new_members_this_month"] = number
		elif "Countries" in category:
			text = li.find("div",{"class":"number_sans"}).text.strip()
			kivaTeam.impact["impact"]["countries"] = text

	# search for the top countires
	top_countries_table = soup.find("ul",{"class":"topCountriesList"})
	top_countries_li = soup.findAll("li",{"class":"topCountry"})
	temp_diction = {}
	for li in top_countries_li:
		percentage_text = li.find("div",{"class":"topCountryPercentage"}).text.replace("%","").strip()
		percentage = float(percentage_text)
		count_text = li.find("div",{"class":"topCountryCount"}).text.strip()[1:-1].replace(",","").strip()
		count = int(count_text)
		name = li.find("div",{"class":"topCountryName"}).text.strip()
		temp_diction[name] = {"percentage":percentage,"count":count}
	kivaTeam.topCountries["top_countries"] = temp_diction.copy()

	return 1


team = KivaTeam()



def run():

	"""
	The main structure of the code. Use to scrape all relevant information from
	the website
	"""


	team_links = []
	################################################################
	# initialize this code block to scrape all team urls into the 
	# team_urls.csv file
	
	# current_page = 1
	# while (getKivaPageLinks(current_page) != -1):
	# 	print "Getting url for page {0}".format(current_page)
	# 	team_links.extend(getKivaPageLinks(current_page))
	# 	current_page = current_page + 1

	# with open("team_urls.csv","wb") as f:
	# 	w = csv.writer(f)
	# 	w.writerow(team_links)
	################################################################

	datafile = open("team_urls.csv","r")
	datareader = csv.reader(datafile, delimiter = ",")
	for row in datareader:
		team_links.extend(row)

	################################################################
	# initialize this code block to create relevant csv files

	# f = open("logfile.txt","wb")
	# f.close()

	# f = open("about.csv","wb")
	# f.close()

	# f = open("loans.csv","wb")
	# f.close()

	# f = open("members.csv","wb")
	# f.close()

	# f = open("impact.csv","wb")
	# f.close()

	# f = open("sectors.csv","wb")
	# f.close()

	# f = open("countries.csv","wb")
	# f.close()

	################################################################

	# initialize this code block to scrape information in intervals

	# with open("lasturl.txt","r") as f:
	# 	last_url = f.readline()
	# last_index = team_links.index(last_url)

	################################################################

	last_index = -1

	firstTime = False
	for link in team_links[last_index+1:]:
		try:



			print "Starting Scrapping Link {0}".format(link)


			

			current_team = KivaTeam()
			setTeamURL(current_team,link)
			setTeamAbout(current_team)
			setTeamLoans(current_team)
			setTeamMembers(current_team)
			setTeamImpact(current_team)

			


			with open("logfile.txt","a") as f:
				f.write(current_team.emptyInAbout())
				f.write(current_team.emptyInLoans())
				f.write(current_team.emptyInMembers())
				f.write(current_team.emptyInImpact())

			with open("about.csv","a") as f:
				for key,value in current_team.getAbout()["about"].items():
					if isinstance(value,basestring):
						current_team.about["about"][key] = value.encode("utf-8")
				w = csv.DictWriter(f,current_team.getAbout()["about"].keys())
				if (firstTime):
					w.writeheader()
				w.writerow(current_team.getAbout()["about"])

			with open("loans.csv","a") as f:
				w = csv.writer(f)
				if (firstTime):
					headers = ["team_url", "loan_id","category","country","raising_status","name","repayment_status"]
					w.writerow(headers)
				for key,value in current_team.getLoans()["loans"].items():
					temp_list = []
					temp_list.append(current_team.url)
					temp_list.append(key)
					temp_list.extend([i.encode("utf-8") for i in current_team.getLoans()["loans"][key].values()])
					w.writerow(temp_list)

			with open("members.csv","a") as f:
				w = csv.writer(f)
				if firstTime:
					headers = ["team_url","team_members","location"]
					w.writerow(headers)
				for name,value in current_team.getMembers()["members"].items():
					w.writerow([current_team.getURL(),name.encode("utf-8"),value.encode("utf-8")])

			with open("impact.csv","a") as f:
				temp_diction = current_team.getImpact()["impact"].copy()
				temp_diction.update({"team_url":current_team.getURL()})
				w = csv.DictWriter(f,temp_diction.keys())
				if (firstTime):
					w.writeheader()
				w.writerow(temp_diction)

			with open("sectors.csv","a") as f:
				temp_diction = current_team.gettopSectors()["top_sectors"].copy()
				headers = ["team_url","top_sectors","number_loans"]
				w = csv.writer(f)
				if (firstTime):
					w.writerow(headers)
				for name,value in temp_diction.items():
					toWrite = [current_team.getURL(),name,value]
					w.writerow(toWrite)

			with open("countries.csv","a") as f:
				temp_diction = current_team.getTopCountries()["top_countries"].copy()
				headers = ["team_url","top_countries","number_loans","percentage"]
				w = csv.writer(f)
				if (firstTime):
					w.writerow(headers)
				for country,values in temp_diction.items():
					num = values["count"]
					percent = values["percentage"]
					toWrite = [current_team.getURL(),country,num,percent]
					w.writerow(toWrite)


			with open("lasturl.txt","wb") as f:
				f.write(link)


			firstTime = False
		except:
			print "Something wrong with link {0}".format(link)
		del current_team

		max_mem_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000
		print "Max memory used {0}".format(max_mem_used)
	
