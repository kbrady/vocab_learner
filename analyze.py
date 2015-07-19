import math
from datetime import timedelta, datetime

def evaluate(word):
	return correct_score(word) / (word.num_times_correct + 1) / time_elapsed(word) * streak_score(word)

def time_elapsed(word):
	return math.log((word.last_seen - datetime(2015,1,1)).total_seconds())

def correct_score(word):
	if word.correct_last_time:
		return 1.0
	else:
		return 50.0

def streak_score(word):
	return 1.0 / ((word.current_streak + 1) * (word.longest_streak + 1))
