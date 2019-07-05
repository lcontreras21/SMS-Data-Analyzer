'''
Luis Contreras-Orendain

Make statistics on the data from SMS messages
Language model will go here

'''
import random
from copy import deepcopy

from analyze import process

# TODO look into further data processing of sms data 
    # like removing punctuation and capitalization
    # , including sentence boundaries
    
# TODO make bigram and unigram creation faster // dont know if its slow yet, untested 4 July 2019

# data is texts separated by TB (text boundary)


def make_bigrams(data):
    # go through the data and make a dict of bigrams
    # data is a list
    bigram_dict = {}
    for index, word in enumerate(data[:-1]):
        bigram = (data[index], data[index + 1])
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    return bigram_dict


# TODO research list comprehension with if/else statements
def make_unigrams(data):
    unigrams = {}
    # probably a faster way to do this
    for word in data:
        if word not in unigrams.keys():
            unigrams[word] = 1
        else:
            unigrams[word] += 1
    return unigrams

# normalizes based on parameter
def bigram_model(bigrams, unigrams, norm=False):
	model = {bigram:(bigrams[bigram] / unigrams[bigram[0]]) for bigram in bigrams}
	if norm:
		bigram_sum = sum(bigram.values())
		model = {bigram:(model[bigram] / bigram_sum) for bigram in model}
	return model

def find_similar_bigrams(model, word):
    # return dict containing bigrams and probability that start with same word
	possible_bigrams = {bigram:model[bigram] for bigram in model.keys() if bigram[0] == word}
    return possible_bigrams

# TODO make it based on person and get text data fromt here
### Answer: make it a function under person class and take data from there

# TODO research how to disable wheel scrolling in vim
def generate_sentence(model, prob=False):
	sentence_length = random.int(1, 10) # longest text
	if prob=True:
        # Make it based on highest probability
		copy_model = deepcopy(model)
		starting_bigram = max(copy_model)[0]
		copy_model.pop(starting_bigram)
		sentence = starting_bigram[0]
		for i in range(sentence_length):
			possible_bigrams = find_similar_bigrams(copy_model, starting_bigram[0])
			next_bigram = max(possible_bigrams)
			starting_bigram = next_bigram
			copy_model.pop(next_bigram)
			sentence += " " + next_bigram[1]
		return sentence
	else:
        # This will be random
        # will make the function long
		# but who cares

		starting_word = random.choice(list(model.keys()))[0]
		sentence = starting_word
		for i in range(sentence_length):
			possible_bigrams = find_similar_bigrams(model, starting_word)
			next_word = random.choice(possible_bigrams))[1]
			sentence += " " + next_word[1]
			starting_word = next_word
		return sentence

def sentence_probability(model, text):
	# if word in text not in model, smooth the probability
	# to include the new word
	prob = 1
	text = text.split()
	min_prob = min(model)
	not_found = []
	for word in text:
		try:
			prob *= model[word]
		except:
			not_found.append(word)
	scaled_prob = min_prob / len(not_found)
	prob *= (len(not_found) * scaled_prob)
	return prob


if __name__ == "__main__":
    print()
