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
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from lang_model import *
from models import *

#This function will handle the reading in and stripping of xml stuff
def load_sms_mms_data():
   # Open XML doc using minidom parser
   #DOMTree = xml.dom.minidom.parse("xml_data/sms_data_processed.xml")
   DOMTree = xml.dom.minidom.parse("xml_data/sms_data.xml")
   collection = DOMTree.documentElement

   #Get all the sms in the collection
   sms = collection.getElementsByTagName("sms")
   mms = collection.getElementsByTagName("mms")
   return sms, mms

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
	
def timeline(people):
	Helena = people["1"]
	Luis = people["2"]
	
	time_stats_H = Helena.time_statistics(print_log=False)
	time_stats_L = Luis.time_statistics(print_log=False)
	time_stats_both = Helena.time_statistics(Luis, print_log=False)

	x_axis_B = list(time_stats_both.keys())
	x_axis_H = list(time_stats_H.keys())
	x_axis_L = list(time_stats_L.keys())

	y_axis_H = [time_stats_H[month][0] for month in x_axis_H]
	y_axis_L = [time_stats_L[month][0] for month in x_axis_L]
	y_axis_B = [time_stats_both[month][0] for month in x_axis_B]

	ax = plt.axes()

	B_ax, = ax.plot(x_axis_B, y_axis_B)
	L_ax, = ax.plot(x_axis_L, y_axis_L)
	H_ax, = ax.plot(x_axis_H, y_axis_H)

	B_ax.set_label("Both")
	L_ax.set_label("Luis")
	H_ax.set_label("Helena")
	ax.legend()

	plt.xticks(rotation=45)
	plt.tight_layout()
	plt.title("Texting history between Helena and Luis from Apr 2019 to the present")
	plt.show()


if __name__ == "__main__":
	people = associate_people()
	timeline(people)
