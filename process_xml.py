### More preprocessing of xml files to handle emoji characters
import re

def convert_to_hex(string):
	# example string would be "&#55358;&#56599"
	string = string.replace("&#", "").replace(";", " ").split()
	string = list(map(int, string))
	
	# Your decimal UTF-16 number (which is in two separate blocks for now) is 55358 56599

	# You subtract 0xd800 from the first block and 0xdc00 from the second to give 0x3e 0x117
	string[0] = string[0] - int("0xd800", 16)
	string[1] = string[1] - int("0xdc00", 16)
	
	# Converting them to binary, padding them out to 10 bits and concatenating them, it's 0b0000 1111 1001 0001 0111
	string = ["{:0>10}".format(bin(i)[2:]) for i in string]
	string = string[0] + string[1] 

	# Then we convert that back to hex, which is 0x0f917
	string = hex(int(string, 2))

	# Finally, we add 0x10000, giving 0x1f917
	string = hex(int(string, 16) + int("0x10000", 16))

	# Therefore, our (hex) HTML entity is &#x1f917;. Or, in decimal, &#129303
	return string

def preprocess_xml(xml_file):
	with open(xml_file[:-4] + "_processed.xml", "w") as new_file:
		with open(xml_file, "r") as old_file:
			for line in old_file:
				matches = re.findall(r"&#[0-9]{6};", line)
				hex_matches = [hex(int(i[2:-1])) for i in matches]

				if len(matches) != 0:
					# the xml data is different now, emojis are in decimal instead of utf 16. Much easier
					#matches = [matches[i] + matches[i+1] for i in range(0, len(matches), 2)]
					#matches = [convert_to_hex(i) for i in matches]

					for i in range(len(matches)):
						line = line.replace(matches[i], hex_matches[i], 1)
				new_file.write(line)

if __name__ == "__main__":
	#convert_to_hex("&#55358;&#56599")
	preprocess_xml("xml_data/sms_data.xml")
