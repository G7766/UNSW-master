import re
import io
import os
import requests
import json
import time
import datetime
from bs4 import BeautifulSoup

def specialisation_list(info):
	acct = re.findall("ACCT[0-9][0-9][0-9][0-9]", info)
	binf = re.findall("BINF[0-9][0-9][0-9][0-9]", info)
	comp = re.findall("COMP[0-9][0-9][0-9][0-9]", info)
	engg = re.findall("ENGG[0-9][0-9][0-9][0-9]", info)
	geos = re.findall("GEOS[0-9][0-9][0-9][0-9]", info)
	gmat = re.findall("GMAT[0-9][0-9][0-9][0-9]", info)
	gsoe = re.findall("GSOE[0-9][0-9][0-9][0-9]", info)
	infs = re.findall("INFS[0-9][0-9][0-9][0-9]", info)
	mark = re.findall("MARK[0-9][0-9][0-9][0-9]", info)
	math = re.findall("MATH[0-9][0-9][0-9][0-9]", info)
	mbax = re.findall("MBAX[0-9][0-9][0-9][0-9]", info)
	tele = re.findall("TELE[0-9][0-9][0-9][0-9]", info)
	subject_list = acct + binf + comp + engg + geos + gmat + gsoe + infs + mark + math + mbax + tele
	return subject_list

#helper function to add created data to db file
def append_specialisation_info_to_db(db, specialisation_id):
	if os.path.isfile('stream.json') and os.access('stream.json', os.R_OK):
		print("stream.json exists and readable.")
		with open('stream.json', 'r') as file:
			data = json.load(file)
			print("File loaded.")
		data.update(db)
		with open('stream.json', 'w') as file:
			file.write(json.dumps(data, indent=4))
			print("Data for " + specialisation_id + " writtten to file")
	else:
		print("Either json file is missing or not readable. Creating stream.json")
		with open('stream.json', 'w') as file:
			file.write(json.dumps(db, indent=4))
			print("Data for " + specialisation_id + " writtten to file")
	return

def crawl_handbook_specialisation(specialisation_id):
	#headers update used to avoid max retries error from the requests module
	#source: stackoverflow
	headers = requests.utils.default_headers()
	headers.update({
    	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

	#request page using beautiful soup
	specialisations_url = 'https://www.handbook.unsw.edu.au/Postgraduate/specialisations/2020/'+ specialisation_id +'?browseByFaculty=FacultyOfEngineering&'
	specialisations_page = requests.get(specialisations_url)
	src = specialisations_page.text
	soup = BeautifulSoup(src,'lxml')

	#crawl specialisation name
	name = soup.find_all("span", {"data-hbui":"module-title"})[0].text
	print('Specialisation name is:\n' + name + '\n')

	#crawl specialisation description
	overview = soup.find_all("div", {"class":"readmore__wrapper"})
	description = ''
	for info in overview:
		description += info.text.strip()
	print('Overview is:\n' + description + '\n')

	#crawl specialisation units of credit
	unit_of_credit = soup.find_all("span", {"class":"hide-xs"})
	for uoc in unit_of_credit:
		if 'Units of Credit' in uoc.text:
			unit_of_credit = uoc.text
			print('UoC:\n' + unit_of_credit + '\n')

	#crawl all data from specialsation structure
	subjects = soup.find_all("div", {"class":"a-card a-card--has-body","data-hbui-filter-key":specialisation_id,"data-hbui-filter-group":"related-courses"})
	for subject in subjects:
		info = subject.text.strip().replace('\n','')

		#crawl Core Courses infomation
		if re.findall("Core Courses", info):
			core_courses = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(core_courses)
			core_course_description = core_courses[1] + '.'
			core_courses_list = specialisation_list(core_courses[2])
			print('Core course description:\n' + core_course_description + '\n')
			print('Core courses are:')
			print(core_courses_list)
			print()

		#crawl Disciplinary Electives infomation
		if re.findall("Disciplinary Electives", info):
			disciplinary_electives = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(disciplinary_electives)
			disciplinary_electives_description = disciplinary_electives[1] + '. ' + disciplinary_electives[2] + '. ' + disciplinary_electives[3] + '.'
			disciplinary_electives_list = specialisation_list(disciplinary_electives[4])
			print('Disciplinary Electives description:\n' + disciplinary_electives_description + '\n')
			print('Disciplinary Electives are:')
			print(disciplinary_electives_list)
			print()

		#crawl Non-Computing Electives infomation
		if (re.findall("Computing Electives", info) or re.findall("COMPUTING ELECTIVES", info)) and re.findall("outside the School", info):
			non_comp_electives = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(non_comp_electives)
			non_comp_electives_description = non_comp_electives[1] + '.'
			non_comp_electives_list = specialisation_list(non_comp_electives[2])
			print('Non-Computing Electives description:\n' + non_comp_electives_description + '\n')
			print('Non-Computing Electives are:')
			print(non_comp_electives_list)
			print()

		#crawl Project Option infomation
		if re.findall("Project Option", info):
			project_option = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(project_option)
			if specialisation_id == 'COMPAS':
				project_option_description = project_option[1] + '.'
				project_option_list = specialisation_list(project_option[2])
			else:
				project_option_description = project_option[1] + '. ' + project_option[2] + '.'
				project_option_list = specialisation_list(project_option[3])
			print('Project Option description:\n' + project_option_description + '\n')
			print('Project Options are:')
			print(project_option_list)
			print()

		#crawl ADK infomation
		if re.findall("ADK", info) or re.findall("Advanced Disciplinary Knowledge Electives", info):
			adk = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(adk)
			adk_description = adk[1] + '.'
			adk_list = specialisation_list(adk[2])
			print('ADK description:\n' + adk_description + '\n')
			print('ADKs are:')
			print(adk_list)
			print()

		#crawl elective (algo and stats) infomation for DS&E stream
		if re.findall("Algorithms and Statistics", info) and re.findall("following courses", info) and (specialisation_id == 'COMPSS'):
			algo_stats = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(algo_stats)
			algo_stats_description = algo_stats[1] + '.'
			algo_stats_list = specialisation_list(algo_stats[2])
			print('Algorithms and Statistics description:\n' + algo_stats_description + '\n')
			print('Algorithms and Statistics electives are:')
			print(algo_stats_list)
			print()

		#crawl elective (db and dm) infomation for DS&E stream
		if re.findall("Databases and Data Mining", info) and re.findall("following courses", info) and (specialisation_id == 'COMPSS'):
			db_dm = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(db_dm)
			db_dm_description = db_dm[1] + '.'
			db_dm_list = specialisation_list(db_dm[2])
			print('Databases and Data Mining description:\n' + db_dm_description + '\n')
			print('Databases and Data Mining electives are:')
			print(db_dm_list)
			print()

		#crawl elective (ml) infomation for DS&E stream
		if re.findall("Machine Learning Information Knowledge", info) and re.findall("following courses", info) and (specialisation_id == 'COMPSS'):
			ml = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(ml)
			ml_description = ml[1] + '.'
			ml_list = specialisation_list(ml[2])
			print('Machine Learning Information Knowledge description:\n' + ml_description + '\n')
			print('Machine Learning Information Knowledge electives are:')
			print(ml_list)
			print()

		#crawl prescribed electives infomation for AI, internetworking and db systems stream
		if re.findall("Prescribed Electives", info) and (specialisation_id in ['COMPAS','COMPDS','COMPIS']):
			prescribed_electives = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(prescribed_electives)
			prescribed_electives_description = prescribed_electives[1] + '.'
			prescribed_electives_list = specialisation_list(prescribed_electives[2])
			print('Prescribed Electives description:\n' + prescribed_electives_description + '\n')
			print('Prescribed Electives are:')
			print(prescribed_electives_list)
			print()

		#crawl prescribed electives infomation for eComm stream
		if re.findall("Prescribed Electives", info) and (specialisation_id in ['COMPES']):
			prescribed_electives = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(prescribed_electives)
			prescribed_electives_description = prescribed_electives[1] + '. ' + prescribed_electives[2] + '. ' + prescribed_electives[3] + '. ' + prescribed_electives[4]+ '.'
			prescribed_electives_list = specialisation_list(prescribed_electives[5])
			print('Prescribed Electives description:\n' + prescribed_electives_description + '\n')
			print('Prescribed Electives are:')
			print(prescribed_electives_list)
			print()

		#crawl prescribed electives infomation for Bioinfomatics stream
		if re.findall("Prescribed Electives", info) and (specialisation_id in ['COMPBS']):
			prescribed_electives = [each_line for each_line in map(str.strip, info.split('.')) if each_line]
			#print(prescribed_electives)
			prescribed_electives_description = prescribed_electives[1] + '. ' + prescribed_electives[2] + '.'
			prescribed_electives_list = specialisation_list(prescribed_electives[3])
			print('Prescribed Electives description:\n' + prescribed_electives_description + '\n')
			print('Prescribed Electives are:')
			print(prescribed_electives_list)
			print()

	#create dictionary with all info for each specialization
	db = {specialisation_id: {
		'name': name,
		'overview': description,
		'minimum units of credit': unit_of_credit,
		'handbook link': specialisations_url,
		'core courses description': core_course_description,
		'core courses list': core_courses_list,
		'ADK description': adk_description,
		'ADK list': adk_list,
		'project option description': project_option_description,
		'project option list': project_option_list,
	}}

	if specialisation_id != 'COMPBS':
		db[specialisation_id]['disciplinary electives description'] = disciplinary_electives_description
		db[specialisation_id]['disciplinary electives list'] = disciplinary_electives_list
		db[specialisation_id]['non-computing electives description'] = non_comp_electives_description
		db[specialisation_id]['non-computing electives list'] = non_comp_electives_list

	if specialisation_id not in ['COMPCS','COMPSS']:
		db[specialisation_id]['prescribed electives description'] = prescribed_electives_description
		db[specialisation_id]['prescribed electives list'] = prescribed_electives_list

	if specialisation_id == 'COMPSS':
		db[specialisation_id]['prescribed elective requirement'] = 'Students must choose at least two courses (12 UOC) from each of two out of the three disciplinary elective lists.'
		db[specialisation_id]['algorithms and statistics description'] = algo_stats_description
		db[specialisation_id]['algorithms and statistics list'] = algo_stats_list
		db[specialisation_id]['databases and data mining description'] = db_dm_description
		db[specialisation_id]['databases and data mining list'] = db_dm_list
		db[specialisation_id]['machine learning information knowledge description'] = ml_description
		db[specialisation_id]['machine learning information knowledge list'] = ml_list

	db[specialisation_id]['timestamp'] = str(datetime.datetime.now())

	append_specialisation_info_to_db(db, specialisation_id)
	return