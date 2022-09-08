import math
import random
from datetime import datetime

bank = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*?+ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*?+'

def generate_api_key():
	key = ''
	key_len = 69
	
	for i in range(key_len):
		index = random.randint(1, len(bank)) - 1
		key += bank[index]
	
	return key

def get_season():
	today = datetime.now()
	year = int(today.strftime('%Y'))
	return year-1 if int(today.strftime('%m')) < 8 else year

def get_year():
	return int(datetime.now().strftime('%Y'))

def get_week():
	aug31 = datetime(get_year(), 8, 31)
	today = datetime.now()
	diff = (today-aug31).days
	week = math.ceil(diff/7)
	return 0 if week < 0 else week

def get_date():
	date = datetime.utcnow()
	return '-'.join([date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')])

if __name__ == '__main__':
	print(generate_api_key())
	print(get_date())
	print(get_season())
	print(get_week())