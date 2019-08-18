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
				Can use that LM to check statistics on words, would be nice to check first usage of X word
'''

from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re

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

	# TODO Make the person iterable based on sms using itertools or something like that, i remember reading about it.

	def __str__(self):
	    return self.type_nos

class Message:	
	def __init__(self, type_no, text, date, readable_date):
		#date in milliseconds Unix time
		self.type_no = type_no
		self.text = text
		self.date = date
		self.readable_date = readable_date

	def __str__(self):
		return str(self.text) + " " + str(self.readable_date)

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
		mms_id = mms.getAttribute("msg_box")
		
		mms_date = mms.getAttribute("date")
		mms_readable_data = mms.getAttribute("readable_date")
		mms_text = ""
		mms_contains_image = False
		mms_count = 0

		part = mms.getElementsByTagName("part")
		for i in part:
			if i.getAttribute("ct") == "image/jpeg":
				mms_contains_image = True
				mms_count += 1
			if i.getAttribute("ct") == "text/plain":
				mms_text = i.getAttribute("text")
		
		current_mms = Photo(person_id, mms_text, mms_date, mms_readable_data)
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
	
	history = Helena.sms_list + Luis.sms_list + Helena.mms_list + Luis.mms_list
	print(len(history))
	history.sort()
	
	with open("chat_history.txt", "w") as f:
		for i in history:
			name = key[i.type_no]
			f.write(name + "\t" + i.readable_date + "\t" + i.text + "\n")
	return
	

# TODO create statistics based on those messages
# TODO create plots and graphs based on those statistics

# TODO create language model based on each person, based on CS 208 lab
if __name__ == "__main__":
	people = associate_people()
	#chat_history(people)
	Helena = people["1"]
	print(Helena.emojis)
