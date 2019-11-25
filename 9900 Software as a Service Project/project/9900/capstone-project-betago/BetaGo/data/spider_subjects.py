import re
import io
import os
import requests
import json
import time
import datetime
from bs4 import BeautifulSoup

#helper function to add created data to db file
def append_subject_info_to_db(db, subject_id):
	if os.path.isfile('db.json') and os.access('db.json', os.R_OK):
		print("db.json exists and readable.")
		with open('db.json', 'r') as file:
			data = json.load(file)
			print("File loaded.")
		data.update(db)
		with open('db.json', 'w') as file:
			file.write(json.dumps(data, indent=4))
			print("Data for " + subject_id + " writtten to file")
	else:
		print("Either json file is missing or not readable. Creating db.json")
		with open('db.json', 'w') as file:
			file.write(json.dumps(db, indent=4))
			print("Data for " + subject_id + " writtten to file")
	return

#main function to crawl data about a given subject
def crawl_handbook_subject(subject_id):
	#headers update used to avoid max retries error from the requests module
	#source: stackoverflow
	headers = requests.utils.default_headers()
	headers.update({
    	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

	#request page using beautiful soup
	subject_url = 'https://www.handbook.unsw.edu.au/Postgraduate/courses/2020/'+ subject_id +'/'
	subject_page = requests.get(subject_url)
	src = subject_page.text
	soup = BeautifulSoup(src,'lxml')

	#crawl subject description
	overview = soup.find_all("div", {"class":"readmore__wrapper"})
	description = ''
	for info in overview:
		description += info.text.strip()
	print('Overview is:\n' + description + '\n')

	#crawl subject name
	name = soup.find_all("span", {"data-hbui":"module-title"})[0].text
	print('Subject name is:\n' + name + '\n')

	#crawl unit of credit
	unit_of_credit = soup.find_all("span", {"class":"hide-xs"})
	for uoc in unit_of_credit:
		if 'Units of Credit' in uoc.text:
			unit_of_credit = uoc.text
			print('UoC:\n' + unit_of_credit + '\n')

	#crawl prerequisites
	conditions_check = soup.select('div .a-card-text')
	if len(conditions_check)> 1:
		prerequisites = soup.find_all("div", {"class":"a-card-text m-toggle-text has-focus"})[0].text.strip().replace('Prerequisite: ', '')
	else:
		prerequisites = 'No prerequisites'
	print('Conditions for enrolment are:\n' + prerequisites + '\n')

	#crawl faculty and school
	data = soup.find_all("a", {"target":"_blank"})
	faculty_found = False
	school_found = False
	for line in data:
		if re.match("^Faculty", line.text) and not faculty_found:
			faculty = line.text
			print('Faculty:\n' + faculty + '\n')
			faculty_found = True
		if re.match("^School", line.text) and not school_found:
			school = line.text
			print('School:\n' + school + '\n')
			school_found = True

	#crawl study level
	study_level = soup.select('.enable-helptext')[1].text
	print('Study Level:\n' + study_level + '\n')

	#crawl offering terms
	offering_terms = soup.find_all('p', {"tabindex":"0","class":""})[0].text
	if not re.match("^Term", offering_terms) and not re.match("^Summer", offering_terms):
		offering_terms = "Not Known"
	print('Offering Terms:\n' + offering_terms + '\n')

	#crawl fees
	#the default fees are overwritten if the fee price can be found on the handbook page
	commonwealth_fees = "$1191"
	domestic_fees = "$4470"
	international_fees = "$5910"
	fees = soup.find_all("p", {"tabindex":"0","class":"muted no-margin"})
	if len(fees) > 0:
		commonwealth_fees = fees[0].text.strip()
		domestic_fees = fees[1].text.strip()
		international_fees = fees[2].text.strip()
		print('Fees:\nCommonwealth: ' + commonwealth_fees + '\nDomestic: '\
			+ domestic_fees + '\nInternational: ' + international_fees+ '\n')

	#crawl course outline link
	course_outline = soup.find_all("div", {"class":"m-button-group m-button-group--list"})
	if len(course_outline) > 0:
		course_outline = course_outline[0].a["href"]
	else:
		course_outline = "Not Available"
	print('Course Outline link:\n' + course_outline + '\n')

	#crawl fees links
	#the default links are overwritten if the actual link can be found from the handbook page
	commonwealth_link = "https://student.unsw.edu.au/fees-student-contribution-rates"
	domestic_link = "https://student.unsw.edu.au/fees-domestic-full-fee-paying"
	international_link = "https://student.unsw.edu.au/fees-international"
	fees_links = soup.find_all("div", {"class":"a-column a-column-df-8 a-column-sm-12"})
	if len(fees_links) > 0:
		commonwealth_link = fees_links[0].a["href"]
		domestic_link = fees_links[1].a["href"]
		international_link = fees_links[2].a["href"]
		print('Links:\nCommonwealth: ' + commonwealth_link + '\nDomestic: '\
			+ domestic_link + '\nInternational: ' + international_link+ '\n')

	#create dictionary with all info for subject
	db = {subject_id: {
		'name': name,
		'overview': description,
		'unit of credit': unit_of_credit,
		'prerequisites': prerequisites,
		'faculty': faculty,
		'school': school,
		'study level': study_level,
		'offering terms': offering_terms,
		'timestamp': str(datetime.datetime.now()),
		'commonwealth fees': commonwealth_fees,
		'domestic fees': domestic_fees,
		'international fees': international_fees,
		'commonwealth link': commonwealth_link,
		'domestic link': domestic_link,
		'international link': international_link,
		'course outline link': course_outline,
		'handbook link': subject_url
	}}

	#calling helper function mentioned before
	append_subject_info_to_db(db, subject_id)
	return

#another helper function to add the timetable info into the db
def append_timetable_info_to_db(subject_id, timetable_url, info):
	if os.path.isfile('db.json') and os.access('db.json', os.R_OK):
		print("db.json exists and readable.")
		with open('db.json', 'r') as file:
			data = json.load(file)
			print("File loaded.")
		data[subject_id]['timetable link'] = timetable_url
		data[subject_id].update(info)
		with open('db.json', 'w') as file:
			file.write(json.dumps(data, indent=4))
			print("Data for " + subject_id + " writtten to file")
	return

#main function used to crawl the timetable details for a given subject
def crawl_class_timetable(subject_id):
	#headers update used to avoid max retries error from the requests module
	#source: stackoverflow
	headers = requests.utils.default_headers()
	headers.update({
    	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    #request page using beautiful soup
	timetable_url = "http://timetable.unsw.edu.au/2020/"+ subject_id +".html"
	timetable_page = requests.get(timetable_url)
	src = timetable_page.text
	soup = BeautifulSoup(src,'lxml')
	print('CRAWLING '+ subject_id)

	#flags
	term_one = False
	term_one_web = False
	term_one_lec = False
	term_two = False
	term_two_web = False
	term_two_lec = False
	term_three = False
	term_three_web = False
	term_three_lec = False
	term_summer = False
	term_summer_web = False
	term_summer_lec = False

	#save important text to list
	data = []
	important = False
	for each_data in soup.find_all("td", {"class":"data"}):
		info = each_data.text.strip()
		if re.match("^Postgraduate", info) or important:
			important = True
			data.append(info)
			#print(info)
		if re.match("^Undergraduate", info):
			important = False

	#parse data from list and extract relevant info
	for index in range(len(data)):
		if re.match("^TERM ONE", data[index]):
			term_one = True
			term_one_lecturer = data[index+5]
			term_one_census = data[index+6]
		if re.match("^TERM TWO", data[index]):
			term_two = True
			term_two_lecturer = data[index+5]
			term_two_census = data[index+6]
		if re.match("^TERM THREE", data[index]):
			term_three = True
			term_three_lecturer = data[index+5]
			term_three_census = data[index+6]
		if re.match("^SUMMER TERM", data[index]):
			term_summer = True
			term_summer_lecturer = data[index+5]
			term_summer_census = data[index+6]
		if re.match("^T1 - Teaching Period One", data[index]) and re.match("^In Person", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_one_lec = True
			term_one_lec_status = data[index+2]
			term_one_lec_capacity = data[index+3]
			term_one_period = data[index+4]
		if re.match("^T1 - Teaching Period One", data[index]) and re.match("^Distance Delivery", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_one_web = True
			term_one_web_status = data[index+2]
			term_one_web_capacity = data[index+3]
			term_one_period = data[index+4]
		if re.match("^T2 - Teaching Period Two", data[index]) and re.match("^In Person", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_two_lec = True
			term_two_lec_status = data[index+2]
			term_two_lec_capacity = data[index+3]
			term_two_period = data[index+4]
		if re.match("^T2 - Teaching Period Two", data[index]) and re.match("^Distance Delivery", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_two_web = True
			term_two_web_status = data[index+2]
			term_two_web_capacity = data[index+3]
			term_two_period = data[index+4]
		if re.match("^T3 - Teaching Period Three", data[index]) and re.match("^In Person", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_three_lec = True
			term_three_lec_status = data[index+2]
			term_three_lec_capacity = data[index+3]
			term_three_period = data[index+4]
		if re.match("^T3 - Teaching Period Three", data[index]) and re.match("^Distance Delivery", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_three_web = True
			term_three_web_status = data[index+2]
			term_three_web_capacity = data[index+3]
			term_three_period = data[index+4]
		if re.match("^U1 - Summer Teaching Period", data[index]) and re.match("^In Person", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_summer_lec = True
			term_summer_lec_status = data[index+2]
			term_summer_lec_capacity = data[index+3]
			term_summer_period = data[index+4]
		if re.match("^U1 - Summer Teaching Period", data[index]) and re.match("^Distance Delivery", data[index+7]) and re.match("^Course Enrolment", data[index+1]):
			term_summer_web = True
			term_summer_web_status = data[index+2]
			term_summer_web_capacity = data[index+3]
			term_summer_period = data[index+4]

	if term_one and (term_one_lec or term_one_web):
		one = {'term one':{
		'lecturer': term_one_lecturer,
		'census date': term_one_census,
		'period': term_one_period}}
		if term_one_lec:
			one['term one']['in person'] = {
			'status': term_one_lec_status,
			'capacity': term_one_lec_capacity
			}
		if term_one_web:
			one['term one']['distance delivery'] = {
			'status': term_one_web_status,
			'capacity': term_one_web_capacity
			}
		print(one)
		print()
		append_timetable_info_to_db(subject_id, timetable_url, one)
			

	if term_two and (term_two_lec or term_two_web):
		two = {'term two':{
		'lecturer': term_two_lecturer,
		'census date': term_two_census,
		'period': term_two_period}}
		if term_two_lec:
			two['term two']['in person'] = {
			'status': term_two_lec_status,
			'capacity': term_two_lec_capacity
			}
		if term_two_web:
			two['term two']['distance delivery'] = {
			'status': term_two_web_status,
			'capacity': term_two_web_capacity
			}
		print(two)
		print()
		append_timetable_info_to_db(subject_id, timetable_url, two)

	if term_three and (term_three_lec or term_three_web):
		three = {'term three':{
		'lecturer': term_three_lecturer,
		'census date': term_three_census,
		'period': term_three_period}}
		if term_three_lec:
			three['term three']['in person'] = {
			'status': term_three_lec_status,
			'capacity': term_three_lec_capacity
			}
		if term_three_web:
			three['term three']['distance delivery'] = {
			'status': term_three_web_status,
			'capacity': term_three_web_capacity
			}
		print(three)
		print()
		append_timetable_info_to_db(subject_id, timetable_url, three)

	if term_summer and (term_summer_lec or term_summer_web):
		summer = {'term summer':{
		'lecturer': term_summer_lecturer,
		'census date': term_summer_census,
		'period': term_summer_period}}
		if term_summer_lec:
			summer['term summer']['in person'] = {
			'status': term_summer_lec_status,
			'capacity': term_summer_lec_capacity
			}
		if term_summer_web:
			summer['term summer']['distance delivery'] = {
			'status': term_summer_web_status,
			'capacity': term_summer_web_capacity
			}
		print(summer)
		print()
		append_timetable_info_to_db(subject_id, timetable_url, summer)
	return

#main function used to add ADK flags to each subject in db
def crawl_adk_subjects():
	#check for files
	if os.path.isfile('adk.txt') and os.access('adk.txt', os.R_OK):
		print("adk.txt exists and readable.")
		if os.path.isfile('db.json') and os.access('db.json', os.R_OK):
			print("db.json exists and readable.")

			#open and load both files
			with open('adk.txt', 'r') as file:
				adk_subjects = [line.strip() for line in file]
				print("adk.txt file loaded.")
			with open('db.json', 'r') as file:
				data = json.load(file)
				print("db File loaded.")

			#update data before upload
			for subject in data:
				if subject in adk_subjects:
					data[subject]['ADK'] = 'true'
				else:
					data[subject]['ADK'] = 'false'

			#upload data back to db
			with open('db.json', 'w') as file:
				file.write(json.dumps(data, indent=4))
				print("All ADK tags updated to file")
	else:
		print("Either adk.txt is missing or not readable. Creating adk.txt")
		#headers update used to avoid max retries error from the requests module
		#source: stackoverflow
		headers = requests.utils.default_headers()
		headers.update({
	    	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	    })

	    #request page using beautiful soup
		information_technology_url = "https://www.handbook.unsw.edu.au/postgraduate/specialisations/2020/COMPCS"
		information_technology_page = requests.get(information_technology_url)
		src = information_technology_page.text
		soup = BeautifulSoup(src,'lxml')

		#crawl all data from specialsation structure
		subjects = soup.find_all("div", {"class":"a-card a-card--has-body","data-hbui-filter-key":"COMPCS","data-hbui-filter-group":"related-courses"})
		important = False
		for subject in subjects:
			info = subject.text.strip()
			if re.findall("ADK", info):
				important = True
			if important and re.findall("COMP", info):
				adk_subjects = re.findall("COMP[0-9][0-9][0-9][0-9]", info)
		print(adk_subjects)

		#load db file and update ADK tag before writing back to db
		if os.path.isfile('db.json') and os.access('db.json', os.R_OK):
			print("db.json exists and readable.")

		with open('db.json', 'r') as file:
			data = json.load(file)
			print("db File loaded.")

		for subject in data:
			if subject in adk_subjects:
				data[subject]['ADK'] = 'true'
			else:
				data[subject]['ADK'] = 'false'

		with open('db.json', 'w') as file:
			file.write(json.dumps(data, indent=4))
			print("All ADK tags updated to file")

		#create adk.txt for future use
		with open('adk.txt', 'w') as file:
			for subject in adk_subjects:
				file.write("%s\n"%subject)
			print("ADK file created and populated")
	return