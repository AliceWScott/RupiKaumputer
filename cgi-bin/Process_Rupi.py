#!/usr/bin/python3
import cgitb; cgitb.enable()
import os 

def process_Rupi():
	path = os.path.dirname(os.path.realpath(__file__)) + '/RupiKaurCorpus.txt'
	f = open(path, 'r').read()
	return f.split('.')
