'''
Luis Contreras-Orendain
Created 6/17/2020

Stores the class definitions for People, SMS, and Message
People will store instances of SMS and Message in a list
'''
import re
from collections import OrderedDict


# This function will create a person class and associate each of the text type to a person
class Person:
	def __init__(self, type_no):
		self.type_no = type_no
		self.sms_list = []
		self.mms_list = []

	def add_sms(self, sms):
		self.sms_list.append(sms)

	def add_mms(self, mms):
		self.mms_list.append(mms)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
		    return self.type_no == other.type_no and len(self.sms_list) == len(other.sms_list)

	def __lt__(self, other):
		return self.type_no < other.type_no

	def __str__(self):
		key = {"1": "Helena", "2": "Luis"}
		return key[self.type_no] + "\tSMS:" + str(len(self.sms_list)) + "\tMMS:" + str(len(self.mms_list)) 
	
	def scan_for_emojis(self):
		self.emojis = {}
		text_data = self.sms_list + self.mms_list
		for ms in text_data:
			matches = re.findall(r"0x[a-z;0-9]{5}", ms.text)
			if len(matches) != 0:
				for match in matches:
					if match not in self.emojis:
						self.emojis[match] = 1
					else:
						self.emojis[match] += 1
	
	def history(self):
		history = self.sms_list + self.mms_list
		history.sort()
		return history

	def time_statistics(self, other="none", print_log=True):
		# Want to compute time statistics with respect to another person
		if (other != "none"):
			history = self.history() + other.history()
		else:
			history = self.history()

		track = OrderedDict()

		for i, ms in enumerate(history):
			history[i] = ms.readable_date.split()

			# current_ms = [month, day, year, time] all strings
			# have it as [day, month, year, time] 
			current_ms = history[i]
			
			# Setting day to be from string to int and removing comma at the end
			history[i][1] = int(current_ms[1][:-1])

			month = current_ms[0] + " " + current_ms[2] # month year
			if month not in track:
				track[month] = [0, OrderedDict()]

			day = current_ms[1]
			if day not in track[month][1]:
				track[month][1][day] = [0, OrderedDict()]

			hour = current_ms[3].split(":")[0]
			if hour not in track[month][1][day][1]:
				track[month][1][day][1][hour] = 0
			
			track[month][0] += 1
			track[month][1][day][0] += 1
			track[month][1][day][1][hour] += 1
		
		# To print out data 
		# Data storage is very confusing, might make a class to handle this tomorrow
		if (print_log):
			for month in track:
				print(month, track[month][0])
				for day in track[month][1]:
					print("\t", day, track[month][1][day][0])
					for hour in track[month][1][day][1]:
						print("\t\t", hour, track[month][1][day][1][hour])
		return track


class Message:	
	def __init__(self, type_no, text, date, readable_date):
		#date in milliseconds Unix time
		self.type_no = type_no
		self.text = text
		self.date = date
		self.readable_date = readable_date

	def __repr__(self):
		return "SMS"

	def __str__(self):
		return self.readable_date + "\n" + self.text

	def __lt__(self, other):
		return self.date < other.date

class Photo:
	def __init__(self, type_no, text, date, readable_date):
		self.type_no = type_no
		self.text = text
		self.date = date
		self.readable_date = readable_date
		self.contains_image = False
		self.photo_count = 0

	def __lt__(self, other):
		return self.date < other.date

	def __repr__(self):
		return "MMS"
