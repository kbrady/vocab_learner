# -*- coding: utf-8 -*-
import random
import sys
import unittest
import analyze
import word
import heap

class TestWord(unittest.TestCase):
	def test_to_str(self):
		w = word.word('çöişüğıÇÖİŞIÜĞasd', 'Testing Turkish Characters', False)
		self.assertEqual(w.text, 'çöişüğıÇÖİŞIÜĞasd')
		self.assertEqual(str(w), 'çöişüğıÇÖİŞIÜĞasd')
	
	def test_guess_word(self):
		word.raw_input = lambda _: give_answer(.5, 'çekirge')
		word.word.say = lambda _: True
		word.display = lambda _: True
		w = word.word('çekirge', 'grasshopper')
		for i in range(2000):
			w.guess_word()
		self.assertEqual(2001, w.num_times_seen)
		self.assertEqual(True, abs(float(w.num_times_correct)/w.num_times_seen - .5) < .03)
		word.raw_input = lambda x: raw_input(x)

class TestHeap(unittest.TestCase):
	def setUp(self):
		self.pl = heap.priority_list()
	
	def test_heap(self):
		word.word.say = lambda _: True
		word.display = lambda _: True
		for pair in [('çekirge', 'grasshopper'), ('okul yılı', 'school year'), ('akort etmek', 'to tune'), ('oynamak', 'to preform'), ('düğmelemek', 'to button'), ('korku', 'fear'), ('memeli', 'mammal'), ('gelir', 'revenue')]:
			text, meaning = pair
			word.raw_input = lambda _: give_answer(.5, text)
			w = word.word(text, meaning)
			heap.heap_node(self.pl, w)
			self.check_values()
		for i in range(20):
			h = self.pl.heap_root
			word.raw_input = lambda _: give_answer(.5, h.word.text)
			h.word.guess_word()
			h.update()
			self.check_values()
	
	def check_values(self):
		try:
			for h in self.pl.word_heap_map.values():
				self.assertEqual(h.value, h.word.evaluate(self.pl.eval_fun))
		except Exception as e:
			print h.word
			print h.word.num_times_seen, h.word.num_times_correct, h.word.last_seen
			print self.pl.get_heap_list()
			raise e

def give_answer(prob, answer):
	if random.random() < prob:
		return answer
	else:
		return 'not ' + answer

if __name__ == '__main__':
	unittest.main()
