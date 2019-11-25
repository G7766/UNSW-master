import os
import time
import datetime
from spider_specialisation import *
from spider_subjects import *

#create a full stream.json
def create_stream_db():
	if os.path.isfile('stream_list.txt') and os.access('stream_list.txt', os.R_OK):
		with open('stream_list.txt', 'r') as file:
			stream_list = [line.strip() for line in file]
		for specialisation in stream_list:
			crawl_handbook_specialisation(specialisation)
			time.sleep(10)
	return

#create a full db.json
def create_course_db():
	if os.path.isfile('course_list.txt') and os.access('course_list.txt', os.R_OK):
		with open('course_list.txt', 'r') as file:
			course_list = [line.strip() for line in file]
		for course_id in course_list:
			crawl_handbook_subject(course_id)
			crawl_class_timetable(course_id)
			time.sleep(10)
		crawl_adk_subjects()
	return

#add new streams into stream.json
def add_to_stream_db():
	if os.path.isfile('stream_list.txt') and os.access('stream_list.txt', os.R_OK):
		if os.path.isfile('stream.json') and os.access('stream.json', os.R_OK):
			with open('stream_list.txt', 'r') as file:
				stream_list = [line.strip() for line in file]
			with open('stream.json', 'r') as file:
				data = json.load(file)
			streams_in_db = []
			for each_stream in data:
				streams_in_db.append(each_stream)
			for stream in stream_list:
				if stream not in streams_in_db:
					crawl_handbook_specialisation(stream)
					time.sleep(10)
	return

#add new courses into db.json
def add_to_course_db():
	if os.path.isfile('course_list.txt') and os.access('course_list.txt', os.R_OK):
		if os.path.isfile('db.json') and os.access('db.json', os.R_OK):
			with open('course_list.txt', 'r') as file:
				course_list = [line.strip() for line in file]
			with open('db.json', 'r') as file:
				data = json.load(file)
			courses_in_db = []
			for each_course in data:
				courses_in_db.append(each_course)
			change = False
			for course in course_list:
				if course not in courses_in_db:
					crawl_handbook_subject(course)
					crawl_class_timetable(course)
					time.sleep(10)
					change = True
			if change:
				crawl_adk_subjects()
	return

#check if an update is required based on timestamp
def update_required(timestamp):
	last_updated = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
	current_date = datetime.date.today()
	difference = current_date - last_updated.date()
	update_after_period = datetime.timedelta(days = 100)
	if difference > update_after_period:
		return True
	else:
		return False



if __name__ == '__main__':
	if os.path.exists('stream.json') and os.path.getsize('stream.json') > 0:
		#check if update required since a non empty stream.json exists
		with open('stream.json', 'r') as file:
			data = json.load(file)
		for each_stream in data:
			timestamp = data[each_stream]['timestamp']
			#update only as needed
			if update_required(timestamp):
				crawl_handbook_specialisation(each_stream)
		#check for new streams to be added
		add_to_stream_db()
	else:
		#create the stream.json and populate fully
		create_stream_db()

	if os.path.exists('db.json') and os.path.getsize('db.json') > 0:
		#check if update required since a non empty db.json exists
		with open('db.json', 'r') as file:
			data = json.load(file)
		update = False
		for each_stream in data:
			timestamp = data[each_stream]['timestamp']
			#update only as needed
			if update_required(timestamp):
				crawl_handbook_subject(each_stream)
				crawl_class_timetable(each_stream)
				time.sleep(10)
				update = True
		if update:
				crawl_adk_subjects()
		#check for new courses to be added
		add_to_course_db()
	else:
		#create the db.json and populate fully
		create_course_db()

	
