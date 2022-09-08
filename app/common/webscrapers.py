import requests
from bs4 import BeautifulSoup
import pandas as pd

from app.common import constants

def scrape_ap_poll():

	response = requests.get(constants.ap_poll_url)
	soup = BeautifulSoup(response.content, 'html.parser')

	rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thread")
	stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
	ranking = [row[2] for row in stats if len(row) >= 3]
	ranking = [team[0:team.index('(')-1] for team in ranking]

	# other = soup.find('div', attrs={'class': 'otherVotes-0-2-140'}).getText()
	
	other = None
	for i in range(100, 250):
		other = soup.find('div', attrs={'class': 'otherVotes-0-2-' + str(i)})
		if other is not None:
			other = other.getText()
			if 'others receiving votes:' in other.lower():
				break

	if other is not None:
		other = other.split(':')[1]
		other = other.split(', ')

		def get_name(arr):
			n = len(arr)
			if (n >= 3):
				name = arr[0]
				for i in range(1, n-1):
					name += ' ' + arr[i]
				return name
			else:
				return arr[0]

		other = [get_name(t.split(' ')) for t in other]
		ranking += other

	ranking = pd.Series(ranking).replace(constants.ap_poll_team_name_replacements[0],
																			 constants.ap_poll_team_name_replacements[1])
	return [r for r in ranking]

def scrape_sagarin_ratings():

	response = requests.get(constants.sagarin_ratings_url)
	soup = BeautifulSoup(response.content, 'html.parser')

	fonts = soup.find('font', attrs={'color': '#000000'}).find_all('font', attrs={'color': '#000000'})
	fonts = [' '.join(f.getText().split()) for f in fonts]
	fonts = [fonts[i] for i in range(2, len(fonts)-3) if i % 2 == 0 and i % 22 != 0]

	def get_name(arr):
		n = len(arr)
		if n == 4:
			return arr[1]
		else:
			return ' '.join(arr[1:-2])

	fonts = [t.split(' ') for t in fonts]
	fonts = [get_name(t) for t in fonts if len(t) >= 4 and t[-2] in ['A', 'a']]

	ranking = pd.Series(fonts).replace(constants.sagarin_ratings_team_name_replacements[0],
																		 constants.sagarin_ratings_team_name_replacements[1])
	return [r for r in ranking]

def scrape_espn_fpi():

	response = requests.get(constants.espn_fpi_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	
	# finds and gets the stat numbers from the html
	rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thread")
	stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
	ranking = [row[0] for row in stats if len(row) == 2]
	ranking = [team.split(' ') for team in ranking]

	def trim_mascots(arr):
		n = len(arr)
		if n == 2:
			return arr[0]
		elif n == 3:
			if ' '.join(arr[1:]) in constants.espn_fpi_double_mascot_names:
				return arr[0]
			else:
				return ' '.join(arr[:2])
		elif n == 4:
			if arr[2] in ['State']:
				return ' '.join(arr[:3])
			else:
				return ' '.join(arr[:2])
		else:
			return ' '.join(arr)

	ranking = [trim_mascots(names) for names in ranking]
	ranking = pd.Series(ranking).replace(constants.espn_fpi_team_name_replacements[0],
																			 constants.espn_fpi_team_name_replacements[1])
	return [r for r in ranking]

def scrape_massey_ratings():
	return []

def scrape_colley_matrix():
	return []