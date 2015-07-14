# -*- coding: utf-8 -*-
import csv
import analize
from word import word

# define the heap
class priority_list:
	def __init__(self, eval_fun=analize.evaluate, title='default'):
		self.eval_fun = eval_fun
		self.title = title
		self.word_heap_map = {}
		self.heap_root = None
		self.border = []
	
	def get_heap_list(self):
		if self.heap_root is None:
			return []
		return self.heap_root.get_list()

class heap_node:
	def __init__(self, parent_heap, word):
		self.parent_heap = parent_heap
		self.word = word
		self.value = self.word.evaluate(self.parent_heap.eval_fun)
		self.parent_heap.word_heap_map[self.word.meaning] = self
		self.parent = None
		self.children = [None, None]
		if self.parent_heap.heap_root is None:
			self.parent_heap.heap_root = self
		else:
			self.parent, order = self.parent_heap.border.pop(0)
			self.parent.children[order] = self
		self.parent_heap.border += [(self, 0), (self,1)]
		# important to do this last so any adjustments in the border are handled correctly
		self.percolate()
	
	def __repr__(self):
		return self.word.__repr__()

	def percolate(self):
		if self.parent is not None and self.parent.value < self.value:
			self.swapWith()
		elif self.children[0] is not None and self.children[0].value > self.value:
			if self.children[1] is not None and self.children[1].value > self.children[0].value:
				self.children[1].swapWith()
			else:
				self.children[0].swapWith()
		elif self.children[1] is not None and self.children[1].value > self.value:
			self.children[1].swapWith()
		else:
			return
		self.percolate()
	
	def swapWith(self):
		# store past parent and previous children
		old_parent = self.parent
		old_children = self.children
		# make our children old_parent and old_parent's other child
		self.children = old_parent.children
		if self.children[0] == self:
			self.children[0] = old_parent
			if self.children[1] is not None:
				self.children[1].parent = self
		else:
			self.children[1] = old_parent
			if self.children[0] is not None:
				self.children[0].parent = self
		# set our parent to be old_parent's past parent
		self.parent = old_parent.parent
		if self.parent_heap.heap_root == old_parent:
			self.parent_heap.heap_root = self
		else:
			if self.parent.children[0] == old_parent:
				self.parent.children[0] = self
			else:
				self.parent.children[1] = self
		# set old_parent's new parent to this node
		old_parent.parent = self
		# set old_parent's children to be our old children
		old_parent.children = old_children
		for c in old_parent.children:
			if c is not None:
				c.parent = old_parent
		# update the border
		if len([x for x in (old_children + self.children) if x is None]) > 0:
			for i in range(len(self.parent_heap.border)):
				if self.parent_heap.border[i][0] == self:
					self.parent_heap.border[i] = (old_parent, self.parent_heap.border[i][1])
				elif self.parent_heap.border[i][0] == old_parent:
					self.parent_heap.border[i] = (self, self.parent_heap.border[i][1])
	
	def update(self):
		self.value = self.word.evaluate(self.parent_heap.eval_fun)
		self.percolate()
	
	def get_list(self):
		# initialize list
		node_list = [(self.value, self.word)]
		# get lists from children
		child_list_0 = []
		child_list_1 = []
		if self.children[0] is not None:
			child_list_0 = self.children[0].get_list()
		if self.children[1] is not None:
			child_list_1 = self.children[1].get_list()
		# merge lists
		while len(child_list_0) + len(child_list_1) > 0:
			if len(child_list_0) == 0:
				node_list += child_list_1
				break
			if len(child_list_1) == 0:
				node_list += child_list_0
				break
			if child_list_0[0][0] > child_list_1[0][0]:
				node_list.append(child_list_0.pop(0))
			else:
				node_list.append(child_list_1.pop(0))
		return node_list

if __name__ == '__main__':
	word_list = priority_list()
	with open('turkish_word_of_the_day.csv', 'rb') as csvfile:
		wordreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		counter = 0
		for row in wordreader:
			counter += 1
			if counter > 6:
				break
			w = word(row[0], row[1])
			heap_node(word_list, w)
	while word_list.heap_root.word.num_times_correct < 5:
		w = word_list.heap_root.word
		w.guess_word()
		word_list.heap_root.update()
