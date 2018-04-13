#!/usr/bin/python3
import cgitb; cgitb.enable()
from markov import MarkovChain
from nltk.tokenize import sent_tokenize
from random import shuffle
from Process_Rupi import process_Rupi
import os
import re
import codecs

class TextProcessor(object):
	
	def __init__(self, sources, order):

		'''
			sources: list of text sources
			order: Markov Chain order. The higher the order, 
				   the more the model "remembers" its history.
		'''

		self.order = order
		self.sentences = self.parse_sources(sources)
		self.markov_chain = MarkovChain(order, self.sentences)
	


	def tokenize(self, text):
		'''
			Custom tokenization function because NLTK's version strips punctuation, which we do not want.
		'''
		return re.findall(r"[\w']+|[.,!?;\n]", text)

	def parse_sources(self, sources):
		'''
			Parses input text, tokenizing it first into sentences, and then words.
			sources: list of text sources.
		'''

		if not isinstance(sources, list):
			raise Exception('ERROR: sources must be a list of strings.')

		sentences = []
		for text in sources:
			sentences.extend(sent_tokenize(text))
		sequences = [self.tokenize(sent) for sent in sentences]
		return sequences

	def remove_plagiarism(self, words, max_overlap):
		'''
			Prevents the model from simply returning a pre-existing input source sentence.
			Returns a Boolean: True if the sentence doesn't exceed overlap ratio, False otherwise.
			Max_overlap: the ratio of words we allow to overlap in a sentence. 
						 The default is 60% (set in generate_sentence())
		'''

		self.full_text = ' '.join([' '.join(words) for words in self.sentences])
		max_overlap = int(max_overlap * len(words))
		ngrams = [words[i:i+max_overlap] for i in range(len(words) - max_overlap + 1)]

		for g in ngrams:
			joined = ' '.join(g)
			if joined in self.full_text and len(joined) > max_overlap:
				return False
		return True


	def generate_sentence(self, 
								seed_string=None,
								max_words=None, 
								min_words=0,
								tries=10, 
								max_overlap=0.6):

		'''
		seed_string: The word we initially start generating from. 
					 If None, the model picks a random word from the set 
					 of words that begin sentences in the input sources.
		max_words: Maximum length of the generated sentence.
		min_words: Minimum length of the generated sentence.
		tries: Number of attempts at generating a sequence. If the model is unable
			   to generate a satisfactory sentence given its parameters, and the number of tries
			   has been exceeded, the function returns None.
		max_overlap: The ratio of words we allow to overlap in a sentence. 
		'''

		def __helper(start_state):

			start_only = False
			if start_state: start_only = True

			''' set the first word of the sentence.'''
			if start_state != None:
				prefix = list(start_state)
				for word in prefix:
					if word == '__START__':
						prefix.pop(0)
					else:
						break
			else:
				start_state = ('__START__',) * self.order
				prefix = []

			''' Try generating a sentence '''
			for x in range(tries):
				words = prefix + self.markov_chain.generate_seq(start_state)
				if max_words and len(words) > max_words:
					continue
				if self.remove_plagiarism(words, max_overlap):
					untupled = []
					for w in words:
						if isinstance(w, tuple):
							untupled.append(' '.join(w))
						else:
							untupled.append(w)
					return ' '.join(untupled)
			return None


		if seed_string is None:
			output = __helper(None)
			if max_words == None: max_words = float('inf')
			if output and (min_words <= len(self.tokenize(output)) <= max_words):
					return output
		else:
			tokens = tuple(self.tokenize(seed_string))
			count = len(tokens)
			
			if count == self.order:
				start_states = [tokens]
			elif 0 < count < self.order:
				if start_only:
					start_states = [tuple('__START__') * (self.order - count) + tokens]
				else:
					start_states = []
					for k in self.markov_chain.states.keys():
						if tuple(filter(lambda x: x != '__START__', k))[:count] == tokens:
							start_states.append(k)
				shuffle(start_states)

			for state in start_states:
				output = __helper(state)
				if output and min_words <= len(self.tokenize(output)) <= max_words:
					return output


def load_from_dir(directory_name):
	''' 
		Takes in the name of a directory of text files, and dumps them into a list of lists. 
		NOTE: this assumes the text directory is in the same directory as this file.
	'''
	data = []
	for filename in os.listdir('./' + directory_name):
		if filename.endswith('.txt'):
			f = open('./' + directory_name + '/' + filename, 'r', errors='ignore').read()
			data.append(f)
	return data

def load_from_filepath(filepath):
	return [codecs.open(filepath, 'r', errors='ignore').read().replace('\r', '\n')]


# corpus = load_from_dir('inaugural')
# corpus = load_from_filepath('./robert_frost.txt')
def runRupi():
	corpus = corpus = load_from_filepath(os.path.dirname(os.path.realpath(__file__)) + '/RupiKaurCorpus.txt')
	tp = TextProcessor(corpus, 2)
	return tp.generate_sentence(seed_string=None, min_words=2, tries=100, max_overlap=0.2)

def runFrost():
	corpus = load_from_filepath(os.path.dirname(os.path.realpath(__file__)) + '/robert_frost.txt')
	tp = TextProcessor(corpus, 2)
	return tp.generate_sentence(seed_string=None, min_words=2, tries=100, max_overlap=0.2)

def runContesse():
	corpus = load_from_filepath(os.path.dirname(os.path.realpath(__file__)) + '/contesse_de_segur.txt')
	tp = TextProcessor(corpus, 2)
	return tp.generate_sentence(seed_string=None, min_words=2, tries=100, max_overlap=0.2)

def testImport():
	return "i do not want to have you\nhave been\nready for you\ncrafted you precisely\nso that s what you do not like most girls\nand men\nthat need a place to rest\na daughter should\nnot have been\ntaught your legs is growing back\nso that s what you do not want to be so complete\ni get from my lips as i answered\ncause people have not\nend you\nare every hope\ni could light a whole city\nand striking the women\naround my hair"
