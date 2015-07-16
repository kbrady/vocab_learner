# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Markup, redirect, url_for
import heap

app = Flask(__name__)
show_word = False
word_list = None
wordreader = None
savefile = None
root = None

@app.route('/')
def home():
	global root
	word_list.save(savefile)
	if show_word:
		return render_template('home.html', meaning=root.word.meaning, word=unicode(root.word.text, 'utf-8'))
	else:
		root = word_list.get_next(wordreader)
		return render_template('home.html', meaning=root.word.meaning, word='')

@app.route('/guess', methods=['GET', 'POST'])
def guess_word():
	global show_word
	word_guessed = request.form['guess']
	w = root.word
	w.say()
	if word_guessed == unicode(w.text, 'utf-8'):
		w.update_stats(not show_word)
		root.update()
		show_word = False
	else:
		show_word = True
	return redirect('/')
	
if __name__ == '__main__':
	savefile = 'turkish.pl'
	word_list, wordreader =	heap.main(savefile, 'turkish_word_of_the_day.csv')
	app.run(debug=True, host='0.0.0.0')
