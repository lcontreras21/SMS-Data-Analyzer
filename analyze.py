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

    def add_sms(sms):
        self.sms_list.append(sms)

    def __str__():
        return "Person "+ str(self.type_no)

class msg:
    def __init__(self, text, date, readable_date):
        #date in milliseconds Unix time
        self.text = text
        self.date = date
        self.readable_date = readable_date
    
    def __str__():
        return str(self.text) + " " + str(self.readable_date)

# Helper function to find current person of sms if not new
def find_person(type_no, people):
    for person in people:
        if person.type_no == type_no:
            return person

def create_people(sms_data):
    # Go through each sms one by one, create people if not created and add to their sms_list if they are created
    people = []
    for sms in sms_data:
        new_person = person(sms.getAttribute("type"))
        if new_person not in people:
            people.append(new_person)
        else:
            new_person = find_person(sms.getAttribute("type"), people)
        
        current_sms = msg(sms.getAttribute("body"), sms.getAttribute("date"), sms.getAttribute("readable_date"))
        print(current_sms)
        new_person.add_sms(current_sms)
    return people

def main():
    print("Loading XML file", flush=True)
    sms_data = process()
    people = create_people(sms_data)
    print(people[0].sms_list)

if __name__ == "__main__":
    main()
