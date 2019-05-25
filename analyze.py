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

#This function will handle the reading in and stripping of xml stuff
def process():
   # Open XML doc using minidom parser
   DOMTree = xml.dom.minidom.parse("sms_data.xml")
   collection = DOMTree.documentElement

   #Get all the sms in the collection
   sms = collection.getElementsByTagName("sms")
   return sms

# This function will create a person class and associate each of the text type to a person
class person:
    def __init__(self, type_no):
        self.type_no = type_no
        self.sms_list = [] 

    def add_sms(self, sms):
        self.sms_list.append(sms)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.type_no == other.type_no
    
    def __lt__(self, other):
        return self.type_no < other.type_no

    def __str__(self):
        return "Person "+ str(self.type_no)

class msg:
    def __init__(self, text, date, readable_date):
        #date in milliseconds Unix time
        self.text = text
        self.date = date
        self.readable_date = readable_date
    
    def __str__(self):
        return str(self.text) + " " + str(self.readable_date)

def create_people(sms_data):
    # create the people found in the text messages
    people = []
    types = []
    for msg in sms_data:
        if msg.getAttribute("type") not in types:
            types.append(msg.getAttribute("type"))
    for type_x in types:
        new_person = person(type_x)
        people.append(new_person)
    return people

def add_messages(people, sms_data):
    # go through each sms and add the text to the appropriate person
    people = people.sort()
    
def main():
    print("Loading XML file", flush=True)
    sms_data = process()
    people = create_people(sms_data)
    for person_x in people.sort():
        print(person_x)

if __name__ == "__main__":
    main()
