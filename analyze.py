'''
I will take in all the text messages me and Helena have sent. I will compile statistics on them and create useful graphs on them.
Additionally, I can use the language model I made for 208 to create an LM for me or for her or for both and create something that makes dialogue.

Outline:
    Done	Read in the xml file containing text.
	Done	Process it so the emojis are readable as xml
    Done	Clean it up to only get the all the sms and mms
				Messages coming from me have type="2" and from her have type="1"
				Photos coming from me have msg_box="2" and from her have msg_box="1" 
				Record all the emojis used in a dictionary to be later looked up online
	Done	Output messages and photos in order they were sent. Faster than scrolling back in the chat
	WIP		Make a binary language model for each person
				Figure out a way to clean the text / if I want toG
				Can use that LM to check statistics on words, would be nice to check first usage of X word
'''

from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re
from collections import OrderedDict


from lang_model import *

#This function will handle the reading in and stripping of xml stuff
def load_sms_mms_data():
   # Open XML doc using minidom parser
   DOMTree = xml.dom.minidom.parse("xml_data/sms_data_processed.xml")
   collection = DOMTree.documentElement

   #Get all the sms in the collection
   sms = collection.getElementsByTagName("sms")
   mms = collection.getElementsByTagName("mms")
   return sms, mms

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

	def time_statistics(self):
		history = self.history()

		track = OrderedDict()

		for i, ms in enumerate(history):
			history[i] = ms.readable_date.split()
			current_ms = history[i]
			history[i][0] = int(current_ms[0])

			month = current_ms[1]
			if month not in track:
				track[month] = [0, OrderedDict()]

			day = current_ms[0]
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
		for month in track:
			print(month, track[month][0])
			for day in track[month][1]:
				print("\t", day, track[month][1][day][0])
				for hour in track[month][1][day][1]:
					print("\t\t", hour, track[month][1][day][1][hour])


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

# Returns a dictionary of people associated to their type value.
# "1" is Helena and "2" is Luis
def associate_people():
	sms_data, mms_data = load_sms_mms_data()
	people = {}

	for sms in sms_data:
		person_id = sms.getAttribute("type")
		if person_id not in people:
			people[person_id] = Person(person_id)

		current_sms = Message(person_id, sms.getAttribute("body"), sms.getAttribute("date"), sms.getAttribute("readable_date"))

		people[person_id].add_sms(current_sms)

	for mms in mms_data:
		mms_date = mms.getAttribute("date")
		mms_readable_data = mms.getAttribute("readable_date")
		mms_text = ""
		mms_contains_image = False
		mms_count = 0

		addrs = mms.getElementsByTagName("addr")
		if addrs[0].getAttribute("address") == "insert-address-token":
			mms_id = "2"
		else:
			mms_id="1"

		part = mms.getElementsByTagName("part")
		for i in part:
			if i.getAttribute("ct") == "image/jpeg":
				mms_contains_image = True
				mms_count += 1
			if i.getAttribute("ct") == "text/plain":
				mms_text = i.getAttribute("text")
		
		current_mms = Photo(mms_id, mms_text, mms_date, mms_readable_data)
		current_mms.contains_image = mms_contains_image
		current_mms.photo_count = mms_count
		
		people[mms_id].add_mms(current_mms)
	
	for person in people:
		people[person].scan_for_emojis()
	return people

# sort both the sms lists and the mms lists and make them play back in order
def chat_history(people):
	Helena = people["1"]
	Luis = people["2"]
	
	key = {"1": "Helena", "2": "Luis"}
	
	history = Helena.history() + Luis.histoy()
	history.sort()
	
	with open("chat_history.txt", "w") as f:
		for i in history:
			name = key[i.type_no]
			f.write(name + "\t" + i.__repr__() + "\t" + i.readable_date + "\t" + i.text + "\n")
	return
	

# TODO create statistics based on those messages
# TODO create plots and graphs based on those statistics
	# TODO count how many messages are sent in a day/week/month/x time unit and get the statistics on those

if __name__ == "__main__":
	people = associate_people()
	Helena, Luis = people["1"], people["2"]
	Helena.time_statistics()
