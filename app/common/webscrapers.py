import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

import app.common.constants as consts

def scrape_ap_poll():

	response = requests.get(consts.ap_poll_url)
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

	ranking = pd.Series(ranking).replace(consts.ap_poll_team_name_replacements[0],
																			 consts.ap_poll_team_name_replacements[1])
	return [r for r in ranking]

def scrape_sagarin_ratings():

	response = requests.get(consts.sagarin_ratings_url)
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

	ranking = pd.Series(fonts).replace(consts.sagarin_ratings_team_name_replacements[0],
																		 consts.sagarin_ratings_team_name_replacements[1])
	return [r for r in ranking]

def scrape_espn_fpi():

	response = requests.get(consts.espn_fpi_url)
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
			if ' '.join(arr[1:]) in consts.espn_fpi_double_mascot_names:
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
	ranking = pd.Series(ranking).replace(consts.espn_fpi_team_name_replacements[0],
																			 consts.espn_fpi_team_name_replacements[1])
	return [r for r in ranking]

def scrape_massey_ratings():

	response = requests.get(consts.massey_ratings_data_enpoint)
	data = response.json()

	def change_st(team_name):
		arr = team_name.split(' ')
		if arr[-1] == 'St':
			arr[-1] = 'State'
		return ' '.join(arr)

	ranking = [change_st(team[0][0]) for team in data['DI']]
	ranking = pd.Series(ranking).replace(consts.massey_ratings_team_name_replacements[0],
																			 consts.massey_ratings_team_name_replacements[1])
	return [r for r in ranking]

def scrape_fei_ratings():

	response = requests.get(consts.fei_ratings_url)
	soup = BeautifulSoup(response.content, 'html.parser')

	rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thread")
	stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
	
	columns = stats[1]
	stats = [t for t in stats if len(t) == len(columns) and t[0] != 'Rk']
	ranking = [t[1] for t in stats]

	ranking = pd.Series(ranking).replace(consts.fei_ratings_team_name_replacements[0],
																			 consts.fei_ratings_team_name_replacements[1])
	return [r for r in ranking]

def scrape_game_schedule(season, week):
	
	url = 'https://www.cbssports.com/college-football/schedule/FBS/{}/{}/{}/'.format(season, 'regular' if week <= 16 else 'postseason', week)

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	dates = soup.findAll('h4')
	dates = [date.getText().strip(' \n') for date in dates]

	rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thread")
	stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
	stats = [[t.strip(' \n') if t.find('-') > -1 else t.strip(' \n0123456789') for t in game] for game in stats]

	def seperate_shortnames(score_string):
		shortnames = score_string.split('-')
		shortnames = [s.strip(' 0123456789/') for s in shortnames]
				
		if shortnames[1][-2:] == 'OT':
			shortnames[1] = shortnames[1][:-2].strip(' 0123456789/')
		
		return shortnames
	
	stats = [arr[:2] + seperate_shortnames(arr[2]) if len(arr) >= 3 else [] for arr in stats if len(arr) <= 0 or (len(arr) >= 3 and arr[2] != 'Postponed' and arr[2] != 'Cancelled')]

	games = list()
	date_index = 0
	game_date = datetime.now()
	
	for game in stats:
		if len(game) <= 0:
			game_date = datetime.strptime(dates[date_index], '%A, %B %d, %Y')
			date_index += 1
		else:
			games.append({
				'date': game_date.strftime('%Y%m%d'),
				'away_team': game[0],
				'home_team': game[1],
				'winner': game[2],
				'loser': game[3]
			})

	return games

def scrape_box_score(date, week, away_team, home_team):

	url = 'https://www.cbssports.com/college-football/gametracker/boxscore/NCAAF_{}_{}@{}/'.format(date, away_team, home_team)

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != "thread")
	stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
	
	box_score = dict()

	try:
		box_score['away_team'] = consts.official_name_lookup.get(stats[1][0].strip(' \n'), away_team)
		box_score['home_team'] = consts.official_name_lookup.get(stats[2][0].strip(' \n'), home_team)

		box_score['date'] = date[:4] + '-' + date[4:6] + '-' + date[6:]
		box_score['week'] = week

		box_score['away_team_statistics'] = dict()
		box_score['home_team_statistics'] = dict()

		start = 3 if stats[3][0] == '1st Downs' else 5
		length = 33

		stats = stats[start:start+length]

		if stats[0][0] != '1st Downs':
			return (None, 'stats name does not match')
		
		# for arr in stats:
		# 	print(arr)

		box_score['away_team_points_scored'] = stats[-2][1:]
		box_score['home_team_points_scored'] = stats[-1][1:]

		box_score['away_team_points_scored'] = [eval(score) for score in box_score['away_team_points_scored']]
		box_score['home_team_points_scored'] = [eval(score) for score in box_score['home_team_points_scored']]

		for i in range(29):
			box_score['away_team_statistics'][consts.cbs_statistics_rename[stats[i][0]]] = stats[i][1]
			box_score['home_team_statistics'][consts.cbs_statistics_rename[stats[i][0]]] = stats[i][2]
		
	except:
		return (None, 'probably index out of bounds')

	try:
		for t in ['away_team_statistics', 'home_team_statistics']:
			tmp_arr = box_score[t]['third_down_conversion'].split('-')
			box_score[t]['third_down_conversion'] = eval(tmp_arr[0]) / eval(tmp_arr[1]) if eval(tmp_arr[1]) > 0 else 1.0

			tmp_arr = box_score[t]['fourth_down_conversion'].split('-')
			box_score[t]['fourth_down_conversion'] = eval(tmp_arr[0]) / eval(tmp_arr[1]) if eval(tmp_arr[1]) > 0 else 1.0

			for key in consts.cbs_statistics_rename.keys():
				if key.find('-') > -1:
					tmp_arr_keys = consts.cbs_statistics_rename[key].split('-')
					tmp_arr_values = box_score[t][consts.cbs_statistics_rename[key]].split('-')
					if len(tmp_arr_values) >= 3 and tmp_arr_values[1] == '':
						tmp_arr_values[-1] = '-' + tmp_arr_values[-1]

					box_score[t][tmp_arr_keys[0]] = eval(tmp_arr_values[0])
					box_score[t][tmp_arr_keys[1]] = eval(tmp_arr_values[-1])

					box_score[t].pop(consts.cbs_statistics_rename[key])

				elif type(box_score[t][consts.cbs_statistics_rename[key]]) is str:
					box_score[t][consts.cbs_statistics_rename[key]] = eval(box_score[t][consts.cbs_statistics_rename[key]])
	except:
		return (None, 'probably eval failure')

	return (box_score, None)