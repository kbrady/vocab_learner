# -*- coding: utf-8 -*-
import os
import csv
from datetime import datetime


class word:
	def __init__(self, text, meaning):
		self.text = text
		self.meaning = meaning
		self.last_seen = None
		self.num_times_seen = 0
		self.num_times_correct = 0
		self.guess_word()
		#self.node = heap.heap_node(self)
	
	def __str__(self):
		return self.text
	
	def say(self):
		os.system("say '" + str(self) + "'")
	
	def guess_word(self, correct=True):
		guess = raw_input(self.meaning + ': ')
		self.say()
		if guess != self.text:
			print self.text
			self.guess_word(correct=False)
		else:
			self.last_seen = datetime.now()
			self.num_times_seen += 1
			if correct:
				self.num_times_correct += 1
	
	def evaluate(self, eval_fun):
		return eval_fun(self)

def read_words(csv_name):
	return True

if __name__ == '__main__':
	word_list = []
	with open('turkish_word_of_the_day.csv', 'rb') as csvfile:
		wordreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in wordreader:
			word_list.append(word(row[0], row[1]))
	while len(word_list) > 0:
		w = word_list.pop(0)
		w.guess_word()
		if w.num_times_correct < 10:
			word_list.append(w)
