import math
from datetime import timedelta, datetime

def evaluate(word):
	time_elapsed = math.log((datetime.now() - word.last_seen).total_seconds())
	return time_elapsed / (word.num_times_correct + 1) * word.num_times_seen
