import math
from datetime import timedelta, datetime

def evaluate(word):
	time_elapsed = math.log((word.last_seen - datetime(2015,1,1)).total_seconds())
	if word.correct_last_time:
		correct_score = 1.0
	else:
		correct_score = 50.0
	return correct_score / (word.num_times_correct + 1) / time_elapsed 
