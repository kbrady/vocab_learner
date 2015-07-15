# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Markup, redirect, url_for
import heap

app = Flask(__name__)
show_word = False
word_list = None
wordreader = None
savefile = None

@app.route('/')
def home():
	if word_list.heap_root is None or word_list.heap_root.word.num_times_correct > 3:
		heap.add_word(wordreader, word_list)
	word_list.save(savefile)
	if show_word:
		return render_template('home.html', meaning=word_list.heap_root.word.meaning, word=unicode(word_list.heap_root.word.text, 'utf-8'))
	else:
		return render_template('home.html', meaning=word_list.heap_root.word.meaning, word='')

@app.route('/guess', methods=['GET', 'POST'])
def guess_word():
	global show_word
	word_guessed = request.form['guess']
	print word_guessed, type(word_guessed)
	w = word_list.heap_root.word
	print w, w.num_times_correct, w.num_times_seen, type(w.text)
	w.say()
	if word_guessed == unicode(w.text, 'utf-8'):
		print 'correct'
		w.update_stats(not show_word)
		word_list.heap_root.update()
		show_word = False
	else:
		print 'wrong'
		show_word = True
	return redirect('/')
	
if __name__ == '__main__':
	savefile = 'turkish.pl'
	word_list, wordreader =	heap.main(savefile, 'turkish_word_of_the_day.csv')
	app.run(debug=True, host='0.0.0.0')
