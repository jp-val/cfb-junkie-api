ap_poll_url = 'https://apnews.com/hub/ap-top-25-college-football-poll'
espn_fpi_url = 'https://www.espn.com/college-football/fpi'
fei_ratings_url = 'https://www.bcftoys.com/2022-fei/'
# massey_ratings_url = 'https://masseyratings.com/cf/fbs/ratings'
sagarin_ratings_url = 'http://sagarin.com/sports/cfsend.htm'

massey_ratings_data_enpoint = 'https://masseyratings.com/json/rate.php?argv=kiqB7tdov4KNhxOtPC9JHm3zh_lITb0Z-0GdxzvAPDb1wPnhbluRKzKy0hSBj-gVP3XmvNm8l6ksrUVUer342g..&task=json'

ap_poll_team_name_replacements = [
	[
		'North Carolina State',
		'Ole Miss',
	],
	[
		'NC State',
		'Mississippi',
	]
]

sagarin_ratings_team_name_replacements = [
	[
		'Southern California',
		'Miami-Florida',
		'Central Florida(UCF)',
		'Miami-Ohio',
		'Army West Point',
		'Florida Atlantic',
		'Hawai\'i',
		'LouisianaMonroe(ULM)',
		'Fla. International'
	],
	[
		'USC',
		'Miami',
		'UCF',
		'Miami (OH)',
		'Army',
		'FAU',
		'Hawaii',
		'UL Monroe',
		'FIU'
	]
]

espn_fpi_team_name_replacements = [
	[
		'Ole Miss',
		'Hawai\'i',
		'Florida Atlantic',
		'Florida International',
		'San José State',
		'UConn',
		'UMass',
	],
	[
		'Mississippi',
		'Hawaii',
		'FAU',
		'FIU',
		'San Jose State',
		'Connecticut',
		'Massachusetts',
	]
]

espn_fpi_double_mascot_names = [
	'Crimson Tide',
	'Golden Gophers',
	'Horned Frogs',
	'Thundering Herd',
	'Black Knights',
	'Eagles',
	'Green Wave',
	'Golden Bears',
	'Ragin\' Cajuns',
	'Fighting Illini',
	'Scarlet Knights',
	'Golden Hurricane',
	'Wolf Pack',
	'Blue Devils',
	'Rainbow Warriors',
]

massey_ratings_team_name_replacements = [
	[
		'Miami FL',
		'WKU',
		'Coastal Car',
		'W Michigan',
		'C Michigan',
		'Ga Southern',
		'Miami OH',
		'FL Atlantic',
		'N Illinois',
		'E Michigan',
		'UT San Antonio',
		'MTSU',
		'Kent',
		'ULM',
		'Florida Intl'
	],
	[
		'Miami',
		'Western Kentucky',
		'Coastal Carolina',
		'Western Michigan',
		'Central Michigan',
		'Georgia Southern',
		'Miami (OH)',
		'FAU',
		'Northern Illinois',
		'Eastern Michigan',
		'UTSA',
		'Middle Tennessee',
		'Kent State',
		'UL Monroe',
		'FIU'
	]
]

fei_ratings_team_name_replacements = [
	[
		'Ole Miss',
		'Florida Atlantic',
		'Southern Mississippi',
		'Florida International'
	],
	[
		'Mississippi',
		'FAU',
		'Southern Miss',
		'FIU'
	]
]