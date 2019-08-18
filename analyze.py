'''
I will take in all the text messages me and Helena have sent. I will compile statistics on them and create useful graphs on them.
Additionally, I can use the language model I made for 208 to create an LM for me or for her or for both and create something that makes dialogue.

Outline:
    Read in the xml file containing text.
    Clean it up to only get the text messages. Contained in <sms protocal... body="messages are here" .../>
    Messages coming from me have type="2" and from her have ty[e="1"

Not being built to handle emojies, future implementation?
'''

from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re


# TODO Figure out how emojis are sent and keep that as a count too, maybe a dict of emoji types and their counts



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
		for sms in self.sms_list:
			matches = re.findall(r"0x[a-z;0-9]{5}", sms.text)
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
    def __init__(self, text, date, readable_date):
        #date in milliseconds Unix time
        self.text = text
        self.date = date
        self.readable_date = readable_date

    def __str__(self):
        return str(self.text) + " " + str(self.readable_date)

class Photo:
	def __init__(self, text, date, readable_date):
		self.text = text
		self.date = date
		self.readable_date = readable_date
		self.contains_image = False
		self.photo_count = 0

# Returns a dictionary of people associated to their type value.
# "1" is Helena and "2" is Luis
def associate_people_to_sms():
	sms_data, mms_data = load_sms_mms_data()
	people = {}

	for sms in sms_data:
		person_id = sms.getAttribute("type")
		if person_id not in people:
			people[person_id] = Person(person_id)

		current_sms = Message(sms.getAttribute("body"), sms.getAttribute("data"), sms.getAttribute("readable_data"))

		people[person_id].add_sms(current_sms)

	for mms in mms_data:
		mms_id = mms.getAttribute("msg_box")
		
		mms_date = mms.getAttribute("date")
		mms_readable_data = mms.getAttribute("readable_data")
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
		
		current_mms = Photo(mms_text, mms_date, mms_readable_data)
		current_mms.contains_image = mms_contains_image
		current_mms.photo_count = mms_count
		
		people[mms_id].add_mms(current_mms)
	
	for person in people:
		people[person].scan_for_emojis()
	return people
	

# TODO create statistics based on those messages
# TODO create plots and graphs based on those statistics

# TODO create language model based on each person, based on CS 208 lab
if __name__ == "__main__":
	people = associate_people_to_sms()
	Helena = people["1"]
	Luis = people["2"]

