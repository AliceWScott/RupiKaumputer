#!/usr/bin/python3
import cgitb; cgitb.enable()
import random
# import gensim.models.keyedvectors as Word2Vec

class MarkovChain(object):

	def __init__(self, order, corpus):

		self.order = order
		self.states = {}
		self.occurs = {}
		# self.model = Word2Vec.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

		for sequence in corpus:

			items = self.order * ['__START__'] + sequence + ['__STOP__']
			for i in range(0, len(sequence) + 1):

				state = tuple(items[i : i + self.order])
				nxt = items[i + self.order]

				if state not in self.states:
					self.states[state] = {}

				# state_synonyms = self.getSynonyms(state)
				# nxt_synonyms = self.getSynonyms(nxt)
				# print(nxt_synonyms)
				# #add synonyms where we add nxt
				# exit()

				# for s in state_synonyms:
				# 	for n in nxt_synonyms:

				# 		self.states[s][n] = self.states[s].get(n, 0) + 1
				# 		self.occurs[s] = self.occurs.get(s,0) + 1

				self.states[state][nxt] = self.states[state].get(nxt, 0) + 1
				self.occurs[state] = self.occurs.get(state,0) + 1

	def getSynonyms(self, word_tuple):
		'''
			Finds all the synonyms for each word in the state tuple.
			Returns a list of tuples containing all permutations of the synonyms
		'''
		synonyms = []
		for w in word_tuple:
			if w != '__START__' and w != '__STOP__':
				synonyms.append([w] + self.model.most_similar(positive=[w], topn=5))
			else:
				synonyms.append([w])
		return list(product(*synonyms))

	def get_next(self, state):
		''' 
		Finds the next state given the words that follow state in the source text.
		'''
		if state[-1] == '__STOP__':
			return 'END'

		index_choice = random.randint(0, self.occurs[state])
		total = 0
		for word, occurences in self.states[state].items():
			if total + occurences >= index_choice:
				return word
			total += occurences
		keys = list(self.states.keys())
		return random.choice(keys)

	def __gen_helper(self, start_state):
		''' 
		Keep adding on a next state from the previous until we reach an end state.
		'''
		if start_state: 
			state = start_state
		else: 
			state = ('__START__',) * self.order

		while(True):
			nxt = self.get_next(state)
			if nxt == 'END':
				break
			else:
				yield nxt
				state = tuple(state[1:]) + (nxt,)

	def generate_seq(self, start_state=None):
		return list(self.__gen_helper(start_state))[:-1]

'''
	Function taken from itertools source code.
	(https://docs.python.org/3/library/itertools.html#itertools.product)
	Itertools is a python3-specific library... this allows for using 2.7 too.
	'''
def product(*args):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
