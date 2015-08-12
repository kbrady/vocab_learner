# -*- coding: utf-8 -*-
import sys
import os
import pickle
import math
from datetime import timedelta, datetime
import csv
import random
from word import word

# define the deck
class deck:
	def __init__(self, lang='tr-TR', max_learn = 20, savefile=None):
		self.lang = lang
		self.learn_in_hour = max_learn
		self.savefile = savefile
		self.word_card_map = {}
		self.next_up = []
		self.to_add = []
		self.done = False
	
	def completed(self):
		return self.done
	
	def add_csv_file(self, csv_name):
		with open(csv_name, 'rb') as csvfile:
			wordreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in wordreader:
				self.add_to_add(row[0], row[1])
		random.shuffle(self.to_add)
	
	def write_words_to_csv(self, filename):
		with open(filename, 'wb') as csvfile:
			wordwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for pair in self.get_all_word_pairs():
				wordwriter.writerow([pair[0].encode('utf-8'), pair[1]])
	
	def add_to_add(self, text, meaning):
		if type(text) == unicode:
			pair = (text, meaning) 
		else:
			pair = (unicode(text, 'utf-8'), meaning) 
		if pair not in self.to_add:
			self.to_add.append(pair)
	
	def get_all_word_pairs(self):
		in_deck = [x.get_word_pair() for x in self.word_card_map.values()]
		full_list = in_deck + [(x[0], x[1], 0) for x in self.to_add]
		full_list.sort()
		return full_list
	
	def delete_word(self, text, meaning):
		if meaning in self.word_card_map:
			self.delete_from_deck(meaning)
		else:
			self.delete_from_to_add(text, meaning)
	
	def change_word(self, new_text, new_meaning, old_text, old_meaning):
		if old_meaning in self.word_card_map:
			# edit existing word and move it in the mapping
			c = self.word_card_map.pop(old_meaning)
			while new_meaning in self.word_card_map:
				new_meaning += ' 2'
			c.edit_word(new_text, new_meaning)
			self.word_card_map[new_meaning] = c
			return
		for i in range(len(self.to_add)):
			pair = self.to_add[i]
			if pair[0] == old_text and pair[1] == old_meaning:
				self.to_add[i] = (new_text, new_meaning)
				return
	
	def delete_from_to_add(self, text, meaning):
		for i in range(len(self.to_add)):
			if self.to_add[i][0] == text and self.to_add[i][1] == meaning:
				self.to_add.pop(i)
				return
	
	def delete_from_deck(self, meaning):
		self.word_card_map[meaning].delete()
	
	def get_deck_list(self):
		return self.word_card_map.values()
	
	def save(self, savefile=None):
		if savefile is None:
			savefile = self.savefile
		with open(savefile, 'wb') as f:
			pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
	
	def review(self, card):
		if len(self.next_up) == 0:
			next_card = self.get_next()
			if next_card == card:
				self.next_up = [card]
				return
			self.next_up = [next_card, card] + self.next_up
			return
		if len(self.next_up) == 1:
			if self.next_up[0] == card:
				return
			self.next_up.append(card)
			return
		self.next_up = [self.next_up[0], card] + self.next_up[1:]
	
	def num_not_known(self):
		return len([x for x in self.word_card_map.values() if x.progress <= 5])
	
	def get_next(self):
		if len(self.next_up) == 0:
			self.next_up = [x for x in self.word_card_map.values() if x.next_schedule <= datetime.now()]
		if len(self.to_add) > 0 and len(self.next_up) == 0 and self.num_not_known() < self.learn_in_hour:
			self.add_word()
			self.next_up = [x for x in self.word_card_map.values() if x.next_schedule <= datetime.now()]
		if len(self.next_up) == 0:
			self.done = True
			return null_card()
		self.done = False
		return self.next_up.pop(0)
	
	def add_word(self):
		pair = self.to_add.pop(0)
		while pair[1] in self.word_card_map:
			if pair[1] != self.word_card_map[pair[1]]:
				self.to_add.append((pair[0],pair[1] + ' 2'))
			if len(self.to_add) == 0:
				return
			pair = self.to_add.pop(0)
		w = word(pair[0], pair[1], False)
		card(self, w)

class card:
	time_steps = [timedelta(seconds=0), timedelta(seconds=5), timedelta(seconds=25), timedelta(minutes=2), timedelta(minutes=10), timedelta(hours=1), timedelta(hours=5), timedelta(days=1), timedelta(days=5), timedelta(days=25)]
	
	def __init__(self, parent_deck, word):
		self.parent_deck = parent_deck
		self.word = word
		self.parent_deck.word_card_map[self.word.meaning] = self
		self.next_schedule = datetime.now()
		self.progress = 0
	
	def __repr__(self):
		return self.word.__repr__()
	
	def correct(self, word_guessed):
		return word_guessed == self.word.text
	
	def get_word_pair(self):
		return (self.word.text, self.word.meaning, self.word.num_times_seen)
	
	def edit_word(self, new_text, new_meaning):
		self.word.text = new_text
		self.word.meaning = new_meaning
	
	def delete(self):
		self.parent_deck.next_up = [x for x in self.parent_deck.next_up if x != self]
		del self.parent_deck.word_card_map[self.word.meaning]
		del self.word

	def update(self):
		if self.word.correct_last_time:
			self.progress += 1
			if self.progress == len(card.time_steps):
				self.progress -= 1
		else:
			self.progress = 0
			self.parent_deck.review(self)
		self.next_schedule = datetime.now() + card.time_steps[self.progress]

class null_card:
	def __init__(self):
		self.word = null_word()
	
	def update(self):
		return None
	
	def correct(self, word_guessed):
		return True

class null_word:
	def __init__(self):
		self.meaning = "Enough practice, go to sleep"
		self.text = "Enough practice, go to sleep"
	
	def update_stats(self, correct):
		return None
	
def main(savefile, lang='tr-TR', max_learn = 20):
	if os.path.exists(savefile):
		with open(savefile, 'rb') as f:
			word_list = pickle.load(f)
			word_list.savefile = savefile
	else:
		word_list = deck(lang, max_learn, savefile)
	return word_list
