# -*- coding: utf-8 -*-
import platform
import sys
import os
import csv
from datetime import datetime

class word:
	def __init__(self, text, meaning, start_guessing=True):
		self.text = text
		self.meaning = meaning
		self.first_added = datetime.now()
		self.last_seen = datetime.now()
		self.correct_last_time = True
		self.longest_streak = 0
		self.current_streak = 0
		self.num_times_seen = 0
		self.num_times_correct = 0
		if start_guessing:
			self.guess_word()
	
	def __str__(self):
		return self.text
	
	def __repr__(self):
		return self.text.encode('utf-8')
	
	def say(self):
		if platform.platform().find('Darwin') == 0:
			os.system("say '" + self.text.encode('utf-8') + "'")
		else:
			os.system("echo '" + self.text.encode('utf-8') + "' | ptts")
	
	def update_stats(self, correct):
		self.last_seen = datetime.now()
		self.num_times_seen += 1
		if correct:
			self.num_times_correct += 1
			self.current_streak += 1
			if self.current_streak > self.longest_streak:
				self.longest_streak = self.current_streak
			self.correct_last_time = True
		else:
			self.correct_last_time = False
			self.current_streak = 0
	
	def guess_word(self, correct=True):
		guess = raw_input(self.meaning + ': ')
		self.say()
		if guess != self.text:
			display(self.text)
			self.guess_word(correct=False)
		else:
			self.update_stats(correct)
	
	def evaluate(self, eval_fun):
		return eval_fun(self)

def display(item):
	print item

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
