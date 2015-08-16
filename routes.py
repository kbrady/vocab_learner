# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Markup, redirect, url_for
import pimsleur
import glob
import datetime

app = Flask(__name__)
show_word = False
word_list = None
root = None
tmp_data = None
languages = ["en-US", "it-IT", "sv-SE", "fr-CA", "de-DE", "he-IL", "tr-TR", "id-ID", "en-GB", "es-AR", "nl-BE", "en-scotland", "ro-RO", "pt-PT", "th-TH", "en-AU", "ja-JP", "sk-SK", "hi-IN", "pt-BR", "hu-HU", "zh-TW", "el-GR", "ru-RU", "en-IE", "es-ES", "nb-NO", "es-MX", "da-DK", "fi-FI", "zh-HK", "ar-SA", "en-ZA", "fr-FR", "zh-CN", "en-IN", "nl-NL", "ko-KR", "pl-PL", "cs-CZ"]

class word_pair:
	def __init__(self, index, pair):
		self.text = pair[0]
		self.meaning = pair[1]
		self.times_seen = pair[2]
		self.index = index
	
	def __repr__(self):
		return str((self.index, self.text, self.meaning))
	
	def __str__(self):
		return self.__repr__()

class word_progress:
	index = 1
	def __init__(self, text, box='', times_seen=0, times_correct=0, longest_streak=0, current_streak=0, last_seen=None, next_schedule=None):
		self.index = word_progress.index
		word_progress.index += 1
		self.text = text
		self.box = box
		self.times_seen = times_seen
		self.times_correct = times_correct
		self.longest_streak = longest_streak
		self.current_streak = current_streak
		if last_seen is None:
			self.last_seen = 'Never'
			self.next_schedule = 'Never'
		else:
			self.last_seen = time_to_streak(last_seen)
			self.next_schedule = time_to_streak(next_schedule)

def time_to_streak(this_time):
	if abs(datetime.datetime.now() - this_time) < datetime.timedelta(hours=10):
		return this_time.strftime("%I:%M %p")
	else:
		return this_time.strftime("%b %d")

@app.route('/', methods=['GET', 'POST'])
def home():
	if word_list is None:
		return redirect('/login')
	if len(word_list.word_card_map) + len(word_list.to_add) == 0:
		return redirect('/upload')
	global root
	global show_word
	completed = word_list.completed()
	if root is None:
		root = word_list.get_next()
		show_word = False
		return render_template('home.html', meaning=root.word.meaning, word='', completed=completed, lang=word_list.lang)
	to_say = ''
	if 'guess' in request.form:
		word_guessed = request.form['guess']
		w = root.word
		to_say = w.text
		if root.correct(word_guessed):
			w.update_stats(not show_word)
			root.update()
			root = word_list.get_next()
			show_word = False
		else:
			show_word = True
	word_list.save()
	if show_word:
		return render_template('home.html', meaning=root.word.meaning, word=root.word.text, completed=completed, say=to_say, lang=word_list.lang)
	else:
		return render_template('home.html', meaning=root.word.meaning, word='', completed=completed, say=to_say, lang=word_list.lang)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if 'user' not in request.form:
		saved_files = glob.glob('*.pdeck')
		saved_files = [x[:x.rfind('.')] for x in saved_files]
		return render_template('login.html', languages=languages, saved_files = saved_files)
	return login(request.form['user'], request.form['lang'])

@app.route('/login/<user_name>', methods=['GET', 'POST'])
def login(user_name):
	print 'test'
	global word_list
	savefile = user_name+'.pdeck'
	lang = request.form.get('lang','tr-TR')
	max_learn = request.form.get('max_learn',20)
	word_list = pimsleur.main(savefile, lang, max_learn)
	return redirect('/')

@app.route('/edit')
def edit_page():
	global tmp_data
	if word_list is None:
		return redirect('/login')
	wp = word_list.get_all_word_pairs()
	tmp_data = [word_pair(i, wp[i]) for i in range(len(wp))]
	return render_template('edit.html', words=tmp_data)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	global tmp_data
	for i in range(len(tmp_data)):
		delete = request.form.get('delete_' + str(i), False)
		text = request.form.get('text_' + str(i), tmp_data[i].text)
		meaning = request.form.get('meaning_' + str(i), tmp_data[i].meaning)
		if delete:
			word_list.delete_word(tmp_data[i].text, tmp_data[i].meaning)
		if text != tmp_data[i].text or meaning != tmp_data[i].meaning:
			word_list.change_word(text, meaning, tmp_data[i].text, tmp_data[i].meaning)
	i = 1
	while request.form.get('text_new_' + str(i), False):
		text = request.form['text_new_' + str(i)]
		meaning = request.form['meaning_new_' + str(i)]
		if len(text) > 0 and len(meaning) > 0:
			word_list.add_to_add(text, meaning)
		i += 1
	word_list.save()
	return edit_page()

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
	if word_list is None:
		return redirect('/login')
	if 'csv_name' not in request.form:
		return render_template('upload.html')
	word_list.add_csv_file(request.form['csv_name'])
	return redirect('/')

@app.route('/download', methods=['GET', 'POST'])
def download_csv_page():
	if word_list is None:
		return redirect('/login')
	if not request.form.get('filename', False):
		return render_template('download.html', username=word_list.savefile[:word_list.savefile.rfind('.')])
	word_list.write_words_to_csv(request.form['filename'])
	return redirect('/')

@app.route('/settings', methods=['GET', 'POST'])
def language_page():
	if word_list is None:
		return redirect('/login')
	if 'lang' not in request.form:
		return render_template('language.html', languages = languages, max_learn = word_list.learn_in_hour)
	word_list.lang = request.form['lang']
	word_list.learn_in_hour = request.form['max_learn']
	word_list.save()
	return redirect('/')

@app.route('/progress')
def progress_page():
	if word_list is None:
		return redirect('/login')
	word_progress.index = 1
	seen_words = [word_progress(x.word.text, x.progress+1, x.word.num_times_seen, x.word.num_times_correct, x.word.longest_streak, x.word.current_streak, x.word.last_seen, x.next_schedule) for x in word_list.get_deck_list()]
	unseen_words = [word_progress(x[0]) for x in word_list.to_add]
	return render_template('progress.html', words = seen_words + unseen_words)

@app.route('/next_up')
def see_next_up():
	if word_list is None:
		return redirect('/login')
	word_progress.index = 1
	next_words = [word_progress(x[1].word.text, x[1].progress+1, x[1].word.num_times_seen, x[1].word.num_times_correct, x[1].word.longest_streak, x[1].word.current_streak, x[1].word.last_seen, x[1].next_schedule) for x in word_list.schedule_manager.queue]
	return render_template('progress.html', words = next_words)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
