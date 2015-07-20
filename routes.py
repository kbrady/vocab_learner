# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Markup, redirect, url_for
import heap

app = Flask(__name__)
show_word = False
word_list = None
savefile = None
root = None

class word_pair:
	def __init__(self, pair):
		self.text = unicode(pair[0], 'utf-8')
		self.meaning = pair[1]

@app.route('/')
def home():
	if word_list is None:
		return redirect('/login')
	global root
	word_list.save(savefile)
	if show_word:
		return render_template('home.html', meaning=root.word.meaning, word=unicode(root.word.text, 'utf-8'))
	else:
		root = word_list.get_next()
		if root is None:
			return render_template('home.html', meaning='UPLOAD WORDS', word='')
		return render_template('home.html', meaning=root.word.meaning, word='')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if 'user' not in request.form:
		return render_template('login.html')
	global word_list
	global savefile
	savefile = request.form['user']+'.pl'
	word_list = heap.main(savefile)
	if len(word_list.word_heap_map) > 0:
		return redirect('/')
	else:
		return redirect('/upload')

@app.route('/edit')
def edit_page():
	if word_list is None:
		return redirect('/login')
	word_pairs = [word_pair(x) for x in word_list.get_all_word_pairs()]
	return render_template('edit.html', words=word_pairs)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	return redirect('/')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
	if word_list is None:
		return redirect('/login')
	if 'csv_name' not in request.form:
		return render_template('upload.html')
	word_list.add_csv_file(request.form['csv_name'])
	return redirect('/')

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
	app.run(debug=True, host='0.0.0.0')
