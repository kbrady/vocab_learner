# -*- coding: utf-8 -*-
import sys
import os
import pickle
import math
from datetime import timedelta, datetime
import csv
import analyze
import random
from word import word

# define the deck
class deck:
	def __init__(self, lang='tr-TR', savefile=None):
		self.lang = lang
		self.word_card_map = {}
		self.boxes = [[] for i in range(5)]
		self.num_boxes = 1
		self.next_up = []
		self.to_add = []
		self.savefile = savefile
	
	def completed(self):
		if len(self.to_add) == 0 and sum([len(b) for b in self.boxes[:(len(self.boxes)-1)]]) == 0:
			return True
		return False
	
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
			self.word_card_map[old_meaning].edit_word(new_text, new_meaning)
			return
		for i in range(len(self.to_add)):
			pair = self.to_add[i]
			if pair[0] == old_text and pair[1] == old_meaning:
				self.to_add[i] = (new_text, new_meaning)
				return
	
	def delete_from_to_add(self, text, meaning):
		for i in range(len(self.to_add)):
			if self.to_add[i][0] == text and self.to_add[i][1]:
				self.to_add.pop(i)
				return
	
	def delete_from_deck(self, meaning):
		self.word_card_map[meaning].delete()
	
	def get_deck_list(self):
		return [val for sublist in self.boxes for val in sublist]
	
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
	
	def get_next(self):
		if len(self.to_add) > 0 and len(self.boxes[0]) == 0:
			self.add_word()
		if len(self.word_card_map) == 0:
			return None
		while len(self.next_up) == 0:
			# only review the final box once per two hour period
			if self.num_boxes >= len(self.boxes):
				self.next_up = [val for sublist in self.boxes[:-1] for val in sublist]
				# if there are some words in the earlier boxes or there are a few words which haven't been seen in two hours
				if len(self.next_up) > 0 or max([datetime.now() - c.word.last_seen for c in self.boxes[-1]]) >= timedelta(hours=2):
					self.next_up += [c for c in self.boxes[-1] if (datetime.now() - c.word.last_seen) >= timedelta(hours=2)]
				else:
					self.next_up += self.boxes[-1]
				self.num_boxes = 1
			else:
				self.next_up = [val for sublist in self.boxes[:self.num_boxes] for val in sublist]
				self.num_boxes = self.num_boxes + 1
			random.shuffle(self.next_up)
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
	def __init__(self, parent_deck, word):
		self.parent_deck = parent_deck
		self.word = word
		self.parent_deck.word_card_map[self.word.meaning] = self
		self.box_index = 0
		self.parent_deck.boxes[self.box_index].append(self)
	
	def __repr__(self):
		return self.word.__repr__()
	
	def get_word_pair(self):
		return (self.word.text, self.word.meaning, self.word.num_times_seen)
	
	def edit_word(self, new_text, new_meaning):
		self.word.text = new_text
		self.word.meaning = new_meaning
	
	def delete(self):
		self.parent_deck.boxes[self.box_index].remove(self)
		self.parent.next_up = [x for x in self.parent.next_up if x != self]
		del self.parent_deck.word_card_map[self.word.meaning]
		del self.word

	def update(self):
		if self.word.correct_last_time:
			if self.box_index == len(self.parent_deck.boxes) - 1:
				return
			new_index = self.box_index + 1
		else:
			self.parent_deck.review(self)
			if self.box_index == 0:
				return
			new_index = max(self.box_index - 2, 0)
		self.parent_deck.boxes[self.box_index].remove(self)
		self.box_index = new_index
		self.parent_deck.boxes[self.box_index].append(self)
	
def main(savefile, lang='tr-TR'):
	if os.path.exists(savefile):
		with open(savefile, 'rb') as f:
			word_list = pickle.load(f)
			word_list.savefile = savefile
	else:
		word_list = deck(lang, savefile)
	return word_list
