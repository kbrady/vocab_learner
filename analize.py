import math
from datetime import timedelta, datetime

def evaluate(word):
	time_elapsed = math.log((word.last_seen - datetime(2015,1,1)).total_seconds())
	return 1.0 / (word.num_times_correct + 1) / time_elapsed 
